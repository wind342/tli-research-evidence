# TLI论文的证据核查规范

**当前论文：** [*Unified Dynamics of Training, Learning, and Inference in Neural Networks*（TLI）](https://github.com/wind342/tli-paper/tree/icml-final/icml)。历史TLIR文件按原版本归档。

**当前论文证据入口：** [TLI_ICML_PAPER_EVIDENCE_MAP.md](TLI_ICML_PAPER_EVIDENCE_MAP.md)  
**原规范建立日期：** 2026-10-25；当前论文核对：2026-11-20。

## 一、先依据论文和记录重建研究事实

核查论文的具体主张、系统与目标、冻结协议、实际实验操作、测量量、数值结果和独立校验。实验事实、解释、数学推导及预测算法的结果分别记录。

当前TLI论文的研究顺序：

1. **九项nanoGPT核心实验**：TL-E01～TL-E08与INF-E01建立实际更新、接收状态、功能响应、分布式功能支撑、能力边界以及冻结推理之间的关系。
2. **预测算法**：TL-E05识别F1、F3、F5条件因素；TL-P01使用已形成的实际更新与响应前信息预测目标边界变化。nanoGPT确认结果为**4,652/5,088，准确率91.43%，四类宏召回91.49%**。
3. **五种附加TLI系统**：ResNet-18、Diffusion U-Net、Vision-MoE、GNN、硬阈值SNN。与nanoGPT合计**六种TLI系统**。
4. **第七种GRU反馈系统**：RL-E05/E06检验正确反馈集中分配、功能支撑变化、已有能力下降与恢复。
5. **统一动力学及14项数学恢复**：从TLI实验建立的方程[T]出发，代入原研究数学模型与条件[A]，得到相应数学关系[R]。ICML正文展示Edge of Stability与Catastrophic Forgetting两项完整推导，另12项位于附录。

四种实验仪器见[EXPERIMENTAL_INSTRUMENTS.md](EXPERIMENTAL_INSTRUMENTS.md)，原生实验与编号见[EXPERIMENT_INDEX.md](EXPERIMENT_INDEX.md)。

## 二、核查对象及实际测量

| 项目 | 应核对的内容 |
|---|---|
| 训练动作 | 已形成的参数更新、接收状态干预、优化器记忆交换 |
| 学习 | 组件联盟、持久支撑重组、能力读出边界、组件版本身份 |
| 推理 | 冻结前向、查询条件支撑、完整logits交互、精确回滚与恢复 |
| TL-P01 | 已形成更新后的目标正确性与四类能力转换 |
| 跨系统实验 | 每种架构的冻结判据、逐种子结果、非线性与支撑指标、预测精度 |
| 强化反馈 | 反馈剂量、训练时长、支撑比例、其他技能margin与准确率、同状态恢复 |
| 数学外推 | 明确的[T]/[A]/[R]入口、原研究条件、符号类型与代数运算 |

### 当前ICML版GNN/SNN数据

以[Windows实验记录](independent_stress_tests/windows_reproduction/README.md)及[机器汇总](independent_stress_tests/windows_reproduction/WINDOWS_REPRODUCTION.json)为准：

| 系统 | 预测准确率 | 四类宏召回率 | 结构判据 |
|---|---:|---:|---|
| GNN | **99.87%**（3,068/3,072） | **97.87%** | **8/9、9/9、8/9**；非线性计数**6/256、36/256、20/256** |
| 硬阈值SNN | **93.24%**（6,713/7,200） | **60.05%** | 四个种子均**12/12** |

GNN预测通过注册判据；SNN预测宏召回低于预定的**90%**阈值，同时四个种子的TLI结构性检验全部通过。独立预测检查文件记录**28个更新事件、10,272条目标记录，PASS**。早期GNN/SNN试验属于不同历史版本。

**RL-E05**较强时序判据为**NOT_SUPPORTED**：12个种子中2个满足时序要求，11项复合判据中10项通过。**RL-E06**使用独立冻结的剂量、时长和恢复协议，保留全部12个正式种子。

## 三、证据层级与核查记录

对每条重要结论，记录五项内容：

1. **论文位置与原命题**：版本、章节、公式/图表、目标和测量定义。
2. **原始实验依据**：冻结合同、代码、模型状态、目标身份和结果文件。
3. **实际观测**：样本量、指标、逐种子分布、负面结果和原判据。
4. **独立检查**：检查器、复算结果、原始文件哈希与证据身份。
5. **科学影响**：该结果具体支持或反驳的命题。

应分别记录三类核验动作：**原生重运行**（实际重新执行训练和干预）、**冻结记录独立复算**、**文件身份及哈希校验**。对应公开程度见[PUBLIC_EVIDENCE_MATRIX.md](PUBLIC_EVIDENCE_MATRIX.md)、[PUBLIC_ARCHIVE.md](PUBLIC_ARCHIVE.md)、[FULL_REPRODUCTION_AUDIT.md](FULL_REPRODUCTION_AUDIT.md)和[REPRODUCIBILITY_NOTES.md](REPRODUCIBILITY_NOTES.md)。

## 四、审稿与文档修改

审稿结论应列出已审阅的论文版本、原始主张、实验依据、支持结果及定位明确的实际差异。每个异议给出具体来源和受影响的命题范围。

排版任务保持科学文字、公式、数据、图表和研究顺序。语言修改保持原命题含义；涉及科学主张的修改须单独说明。当前TLI论文以[论文源码](https://github.com/wind342/tli-paper/tree/icml-final/icml)与[ICML证据地图](TLI_ICML_PAPER_EVIDENCE_MAP.md)为准。
