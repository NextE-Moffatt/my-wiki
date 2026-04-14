# arXiv

_最后更新：2026-04-14_

## 概述  
arXiv 是一个始于 1991 年的学术论文预印本平台，专注数学、计算机科学、物理学等领域，论文需用 LaTeX 编写；在 Llama 预训练数据中占比 2.5%，是大模型获取前沿科技知识的核心结构化语料。

## 详细内容  
根据《百面大模型》第 2.1 节，arXiv 数据集的技术要点如下：

- **运营主体与历史**：1991 年由 Paul Ginsparg 创建，现由康奈尔大学运营；  
- **内容范围**：覆盖 cs（计算机科学）、math（数学）、physics（物理）、stat（统计）、quant-ph（量子物理）等学科；  
- **格式要求**：所有提交论文必须使用 LaTeX 编译，确保公式、图表、参考文献结构高度规范；  
- **在 Llama 中的配比**：占预训练语料 **2.5%**；  
- **数据价值**：  
  - 提供高质量、逻辑严密、术语精准的技术文本，强化模型对专业概念（如 “transformer”, “backpropagation”）的深层理解；  
  - LaTeX 源码中蕴含丰富的语义结构（section, equation, theorem），可辅助模型学习学术写作范式；  
- **清洗难点**：  
  - 需解析 LaTeX 源码（非 PDF），提取 clean text；  
  - 过滤低质量预印本（如未完成稿、重复提交）；  
  - 处理公式符号（如 `$\alpha$` → “alpha” 或保留为 token）。

该数据集与 `datasets/pubmed_central`（生物医学）形成学科互补，共同构成大模型的**科研知识底座**。

## 相关页面  
[[datasets/pubmed_central]]  
[[datasets/c4]]  
[[concepts/latex_parsing]]  
[[concepts/technical_writing]]  
[[models/llama]]

## 来源  
《百面大模型》，第 2.1 节 “大模型训练开源数据集”，2025 年出版；含 arXiv 起始年份（1991）、学科范围、LaTeX 要求、Llama 配比（2.5%）。