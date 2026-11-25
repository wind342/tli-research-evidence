"""Download, join and verify the nanoGPT three-history evidence archive."""
from pathlib import Path
import argparse, hashlib, json, shutil, urllib.request

def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('TLI_nanoGPT_Three_History_Evidence.parts.json'))
    parser.add_argument('--directory',type=Path,default=Path.cwd())
    parser.add_argument('--download',action='store_true')
    args=parser.parse_args()
    doc=json.loads(args.manifest.read_text(encoding='utf-8'))
    directory=args.directory.resolve();directory.mkdir(parents=True,exist_ok=True)
    for item in doc['parts']:
        assert Path(item['name']).name==item['name']
        path=directory/item['name']
        if not path.exists() and args.download:
            partial=path.with_suffix(path.suffix+'.partial')
            with urllib.request.urlopen(item['url']) as source,partial.open('xb') as target:
                shutil.copyfileobj(source,target,1024*1024)
            assert partial.stat().st_size==item['bytes'] and digest(partial)==item['sha256'],item['name']
            partial.rename(path)
        assert path.is_file(),f'Download {item["name"]} or pass --download'
        assert path.stat().st_size==item['bytes'] and digest(path)==item['sha256'],item['name']
        print('Verified',item['name'],flush=True)
    assert Path(doc['archive']).name==doc['archive']
    joined=directory/doc['archive']
    if not joined.exists():
        partial=joined.with_suffix('.partial.zip')
        with partial.open('xb') as target:
            for item in doc['parts']:
                with (directory/item['name']).open('rb') as source:shutil.copyfileobj(source,target,1024*1024)
        assert partial.stat().st_size==doc['bytes'] and digest(partial)==doc['sha256']
        partial.rename(joined)
    assert joined.stat().st_size==doc['bytes'] and digest(joined)==doc['sha256']
    print('Verified archive:',joined)

if __name__=='__main__':main()
