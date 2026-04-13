# arXiv

_最后更新：2026-04-13_

## 概述  
arXiv 是1991年建立的开放获取预印本平台，聚焦数学、计算机科学、物理学等领域，其**LaTeX 源码结构化、高术语密度、强逻辑连贯性**，使其成为大模型科学推理能力的基石语料。

## 详细内容  
- **数据特性**：  
  - 截至2023年：收录 **240万+** 篇论文，日均新增约 1,800 篇；  
  - 计算机科学子集（cs.*）占比 38%，其中 `cs.CL`（计算语言学）占 12.4%，`cs.LG`（机器学习）占 21.7%；  
  - 元数据完备：标题、作者、摘要、分类（ACM CCS codes）、引用关系（via `arXiv` API）。  
- **文本处理流程**：  
  - 输入：`.tar.gz` LaTeX 源码包；  
  - 解析：`latexml` 编译为 XHTML，提取 `<abstract>`/`<section>`/`<equation>`；  
  - 清洗：移除 `\begin{proof}...\end{proof}`（冗余）、参考文献（`bibliography` 环境）、附录；  
  - 保留：定理环境（`theorem`, `lemma`）、公式（MathML → `\\frac{a}{b}`）、算法伪代码（`algorithmic` 环境）。  
- **在 Llama-2 中的权重**：**2.5%**（仅限 cs.CL / cs.LG / math.ST / physics.comp-ph 子集）；消融显示移除 arXiv 导致 `MMLU-STEM` 分数下降 4.1%，`Big-Bench-Hard` 中 `Logical Deduction` 下降 6.8%。  
- **局限性**：  
  - 无 peer-review 保证，存在错误传播风险（如早期 Transformer 论文 typo）；  
  - LaTeX → text 转换损失公式语义（如 `\nabla` → `nabla`）；  
  - 中文 arXiv（CNKI 预印）未被主流模型采用。

## 相关页面  
[[datasets/pubmed_central]] [[models/llama]] [[concepts/scientific_reasoning]] [[tools/latexml]] [[concepts/mathematical_notation]]

## 来源  
《百面大模型》，第2章，第50页（2025）；Llama-2 Technical Report (Meta, 2023)；arXiv API Documentation (2023).