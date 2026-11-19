#!/usr/bin/env python3
"""21 independent algebra/numerical spot checks for the fourteen TLI recoveries.

These checks validate representative identities under stated original-model
assumptions; they do not prove the complete original papers or replay experiments.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp


def close(x, y, atol):
    if not np.allclose(x, y, atol=atol, rtol=atol):
        raise AssertionError(f"mismatch: {x!r} vs {y!r}")


def run(inp, derivations):
    results = []
    atol = inp['atol']
    def check(case, name, fn):
        try:
            fn()
            results.append({'case': case, 'name': name, 'status': 'PASS'})
        except Exception as exc:
            results.append({'case': case, 'name': name, 'status': 'FAIL', 'error': str(exc)})

    def edge_modes():
        x = inp['edge']; eta = x['eta']; lam = np.asarray(x['eigenvalues'])
        H = np.diag(lam); e = np.array([0.2, -0.7]); after = e - eta * H @ e
        close(after, (1 - eta * lam) * e, atol)
    check(1, 'local Hessian eigenmode multiplier', edge_modes)

    def edge_threshold():
        eta = inp['edge']['eta']; lam = 2 / eta
        close(1 - eta * lam, -1, atol)
        assert abs(1 - eta * (lam + 1e-2)) > 1
        assert abs(1 - eta * (lam - 1e-2)) < 1
    check(1, 'positive-curvature stability boundary', edge_threshold)

    def logistic():
        eta = inp['implicit']['eta']; w = inp['implicit']['w']; W = inp['implicit']['large_w']
        d = eta / (1 + math.exp(w)); D = eta / (1 + math.exp(W))
        assert d > 0 and D > 0
        close(math.expm1(D) * math.exp(W), eta, 1e-7)
    check(2, 'continued logistic update and exponential increment limit', logistic)

    def binomial_moments():
        x = inp['collapse']; M, q = x['M'], x['q']; ks = np.arange(M + 1)
        ps = np.array([math.comb(M, int(k)) * q**k * (1 - q)**(M-k) for k in ks]); freq = ks/M
        close(ps.sum(), 1, atol); close((freq * ps).sum(), q, atol)
        close((((freq-q)**2)*ps).sum(), q*(1-q)/M, atol)
        close(ps[0], (1-q)**M, atol)
    check(3, 'finite binomial support-loss probability, mean and variance', binomial_moments)

    def mixture():
        x = inp['collapse']; alpha, q0, r, t = x['alpha'], x['q0'], x['r'], x['generations']
        q = q0
        for _ in range(t): q = (1-alpha)*q + alpha*r
        close(q, r+(1-alpha)**t*(q0-r), atol)
        close(1-(1-alpha*r)**x['M'], 1-(1-alpha*r)**x['M'], atol)
        assert 0 < 1-(1-alpha*r)**x['M'] < 1
    check(3, 'real-data mixture recurrence and category recovery', mixture)

    def spectral():
        x = inp['spectral']; lam = np.array(x['eigenvalues']); eta = x['eta']; steps = x['steps']
        r = np.array(x['residual'])
        for _ in range(steps): r = r - eta * lam * r
        close(r, (1-eta*lam)**steps*np.array(x['residual']), atol)
    check(4, 'fixed-kernel modal residual decay', spectral)

    def benign():
        x = inp['benign']; X = np.asarray(x['X']); beta = np.asarray(x['beta']); Sigma = np.diag(x['covariance']); s2 = x['sigma2']
        G = np.linalg.inv(X @ X.T); P = X.T @ G @ X; bias = -(np.eye(X.shape[1])-P) @ beta
        noise_columns = X.T @ G * math.sqrt(s2)
        analytical = bias @ Sigma @ bias + s2*np.trace(Sigma @ X.T @ G @ G @ X)
        independently_expanded = bias @ Sigma @ bias + sum(v @ Sigma @ v for v in noise_columns.T)
        close(analytical, independently_expanded, atol)
        close(X @ (X.T @ G @ (X @ beta)), X @ beta, atol)
    check(5, 'minimum-norm conditional expected bias/variance risk', benign)

    def chinchilla_balance():
        x = inp['chinchilla']; a,b,A,B,C = (x[k] for k in ('alpha','beta','A','B','compute'))
        n = ((a*A)/(b*B))**(1/(a+b))*(C/6)**(b/(a+b)); d=C/(6*n)
        close(a*A*n**(-a), b*B*d**(-b), atol)
        close(a*A*n**(-a-1)-b*B*d**(-b)/n, 0, atol)
    check(6, 'compute-constrained marginal balance', chinchilla_balance)

    def chinchilla_scaling():
        x = inp['chinchilla']; a,b,A,B,C = (x[k] for k in ('alpha','beta','A','B','compute'))
        def opt(C0):
            N=((a*A)/(b*B))**(1/(a+b))*(C0/6)**(b/(a+b)); return A*N**(-a)+B*(C0/(6*N))**(-b)
        close(opt(4*C)/opt(C), 4**(-a*b/(a+b)), atol)
    check(6, 'optimized-loss power-law scaling conditional on empirical input', chinchilla_scaling)

    def isometry():
        J=np.array(inp['isometry']['J']); v=np.array(inp['isometry']['null_vector'])
        close(J@v, np.zeros(J.shape[0]), atol)
        positive=np.linalg.svd(J, compute_uv=False)
        assert min(positive)>0 and np.linalg.matrix_rank(J)<J.shape[1]
    check(7, 'Jacobian nullspace has zero full-space minimum gain', isometry)

    def dropout_moments():
        x = inp['dropout']; w=np.array(x['w']); v=np.array(x['x']); r=x['keep_probability']; scores=[]; probs=[]
        for mask in itertools.product((0,1),repeat=len(w)):
            a=np.asarray(mask); probs.append(np.prod(np.where(a==1,r,1-r))); scores.append(w@(v*a/r))
        ps=np.array(probs); zs=np.array(scores); mu=w@v
        close(ps@zs,mu,atol)
        close(ps@((zs-mu)**2),(1-r)/r*np.sum((w*v)**2),atol)
    check(8, 'exhaustive independent dropout mean and variance', dropout_moments)

    def dropout_regularizer():
        x=inp['dropout']; w=np.array(x['w']); v=np.array(x['x']); r=x['keep_probability']; target=.23
        expected=0
        for mask in itertools.product((0,1),repeat=len(w)):
            a=np.asarray(mask); prob=np.prod(np.where(a==1,r,1-r)); expected+=prob*.5*(w@(v*a/r)-target)**2
        base=.5*(w@v-target)**2
        close(expected-base,.5*(1-r)/r*np.sum((w*v)**2),atol)
    check(8, 'exact Gaussian-linear dropout penalty', dropout_regularizer)

    def forgetting():
        x=inp['forgetting']; m=x['initial_margin']; r=x['responses']; states=[m]
        for v in r: states.append(states[-1]+v)
        close(states[-1],m+sum(r),atol)
        assert states[0]>0 and states[-1]<=0 and (sum(r)<=-m)
    check(9, 'telescoping response and capability boundary crossing', forgetting)

    def grokking_evolution():
        x=inp['grokking']; cov=np.array(x['covariance']); D=np.array(x['initial_difference']); eta=x['eta0']; t=x['time']
        Dt=np.exp(-2*eta*cov*t)*D
        Ltr=Dt@np.diag(cov)@Dt; Lgen=Dt@Dt
        close(Ltr,sum(D*D*cov*np.exp(-4*eta*cov*t)),atol)
        close(Lgen,sum(D*D*np.exp(-4*eta*cov*t)),atol)
    check(10, 'shared-state train/generalization gradient-flow readouts', grokking_evolution)

    def grokking_delay():
        x=inp['grokking']; lam=x['lambda_ratio']; eta=x['eta0']; nu=(1-math.sqrt(lam))**2
        k=4*eta*nu; target=.13; amp=.92
        ttr=math.log(amp/target)/k; tgen=math.log(amp/(nu*target))/k
        close(tgen-ttr,-math.log(1-math.sqrt(lam))/(2*eta*nu),atol)
        assert tgen>ttr
    check(10, 'spectral-edge shared-exponent crossing delay', grokking_delay)

    def mup():
        x=inp['mup']; c=x['c']; chi=x['loss_gradient']; a=[]
        for n in x['widths']:
            v=np.full(n,n**(-.5)); hnorm2=n
            dh=-n**(-c-.5)*chi*v*hnorm2
            df=-n**(-c-1)*chi*np.dot(v,v)*hnorm2
            close(dh[0],-chi*n**(-c),atol); close(df,-chi*n**(-c),atol)
            a.append(df)
        close(a[1]/a[0],(x['widths'][1]/x['widths'][0])**(-c),atol)
    check(11, 'specified one-step width-scaling identity', mup)

    def sam_hessian():
        x=inp['sam']; a,b,c=x['a'],x['b'],x['reparameterization']
        assert a*b==1
        H=np.array([[b*b,a*b],[a*b,a*a]])
        evals=np.linalg.eigvalsh(H); close(evals[-1],a*a+b*b,atol); close(evals[0],0,atol)
        close((c*a)*(b/c),a*b,atol)
        close((c*a)**2+(b/c)**2,np.linalg.eigvalsh(np.array([[(b/c)**2,a*b],[a*b,(c*a)**2]]))[-1],atol)
    check(12, 'function-preserving SAM/sharpness Hessian reparameterization', sam_hessian)

    def sam_response():
        x=inp['sam']; a,b,eta,rho=x['a']+.1,x['b'],x['eta'],x['rho']
        g=(a*b-1)*np.array([b,a]); e=rho*g/np.linalg.norm(g)
        aa,bb=np.array([a,b])+e
        da=-eta*(aa*bb-1)*bb; db=-eta*(aa*bb-1)*aa
        exact=(a+da)*(b+db)-a*b
        recovered=-eta*(aa*bb-1)*(b*bb+a*aa)+eta**2*(aa*bb-1)**2*aa*bb
        close(exact,recovered,atol)
        sgd_da,sgd_db=-eta*(a*b-1)*np.array([b,a]); sgd_exact=(a+sgd_da)*(b+sgd_db)-a*b
        close(sgd_exact,-eta*(a*b-1)*(a*a+b*b)+eta**2*(a*b-1)**2*a*b,atol)
    check(12, 'one-step SGD and SAM realized functional responses', sam_response)

    def noise_projection():
        x=inp['noise']; S=np.array(x['covariance']); j=np.array(x['readout_gradient']); eta=x['eta']; B=x['batch']
        xform=-eta*np.eye(2)
        cov_action=xform@(S/B)@xform.T
        close(cov_action,eta**2*S/B,atol)
        close(j@cov_action@j,eta**2/B*(j@S@j),atol)
        close(-eta*j@np.array(x['gradient_mean']),-eta*np.dot(j,x['gradient_mean']),atol)
    check(13, 'minibatch action covariance and target Jacobian projection', noise_projection)

    def double_monte_carlo():
        x=inp['double']; rng=np.random.default_rng(inp['seed']); trials=inp['monte_carlo_trials']; sigma2=x['sigma2']
        for label in ('under','over'):
            n,p=x[label]['n'],x[label]['p']; vals=[]
            for _ in range(trials):
                X=rng.standard_normal((n,p))
                gram=X.T@X if p<n else X@X.T
                vals.append(sigma2*np.trace(np.linalg.inv(gram)))
            expected=sigma2*(p/(n-p-1) if p<n else n/(p-n-1))
            rel=abs(np.mean(vals)-expected)/expected
            if rel>inp['relative_monte_carlo_tolerance']:
                raise AssertionError(f'{label}: relative error {rel:.4g} exceeds tolerance')
    check(14, 'seeded inverse-Wishart expected excess-risk Monte Carlo on both sides', double_monte_carlo)

    def double_symbols():
        s=derivations.split('### 5.2.14 Double Descent:',1)[1]
        assert r'R_{t,\mathrm{test}}' in s
        assert r'\mathcal E_{\mathrm{test}}' in s
        assert s.count(r'\mathbb E[\mathcal E_{\mathrm{test}}]')>=4
        assert r'\mathbb ER' not in s and r'\mathbb E R' not in s
        # Response and expected risk have different meanings, including opposite
        # sign when m_test := -E_test.
        assert r'm_{\mathrm{test}}(L)=-\mathcal E_{\mathrm{test}}(L)' in s
    check(14, 'TLI response and expected excess-risk notation separation', double_symbols)

    return results


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs',type=Path,default=Path(__file__).with_name('inputs.json'))
    ap.add_argument('--derivations',type=Path,default=Path(__file__).resolve().parents[1]/'theory/TLI_THEORY_FIRST_14_DERIVATIONS.md')
    ap.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULTS.json'))
    args=ap.parse_args()
    raw=args.inputs.read_bytes(); data=json.loads(raw)
    source=args.derivations.read_bytes(); findings=run(data,source.decode('utf-8'))
    counts={k:sum(x['status']==k for x in findings) for k in ('PASS','FAIL')}
    output={'schema':'tli-math-audit-v1','kind':'NEW_INDEPENDENT_CHECKS_NOT_HISTORICAL_SCRIPT','checks':len(findings),**counts,'input_sha256':hashlib.sha256(raw).hexdigest(),'cases':findings,'numpy':np.__version__,'sympy':sp.__version__}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"TLI mathematical checks: {counts['PASS']}/{len(findings)} PASS, {counts['FAIL']} FAIL")
    for row in findings: print(f"{row['status']} case {row['case']:02d} {row['name']}"+(f": {row['error']}" if 'error' in row else ''))
    return int(counts['FAIL']>0 or len(findings)!=21)

if __name__=='__main__':
    raise SystemExit(main())
