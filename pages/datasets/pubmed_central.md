# PubMed Central

_最后更新：2026-04-14_

## 概述  
PubMed Central（PMC）是美国国家卫生研究院（NIH）运营的免费生物医学文献全文数据库，收录约 500 万份论文/期刊，是大模型获取生命科学专业知识的核心语料；虽未在 Llama 配比中提及，但被明确列为大模型预训练重要数据源。

## 详细内容  
依据《百面大模型》第 2.1 节，PMC 的关键事实如下：

- **运营机构与规模**：由 NIH 下属 NLM 运营，收录约 **500 万份** 生物医学领域学术论文或期刊全文；  
- **内容特征**：  
  - 覆盖临床医学、基础研究、药物开发、基因组学等细分方向；  
  - 文本高度专业化，含大量实体（如 gene names: *TP53*, drug names: *aspirin*）、关系（如 “EGFR mutation causes lung cancer”）与实验范式；  
- **结构化优势**：  
  - 多数论文以 XML 格式存档（JATS 标准），标题、摘要、方法、结果、讨论等 section 清晰可提取；  
  - 支持精准段落级切分，利于 instruction tuning 数据构造；  
- **与 arXiv 对比**：  
  - arXiv：计算机/物理/数学，预印本，LaTeX 格式，更新快；  
  - PMC：生物医学，经同行评议的正式出版物，XML 格式，术语更稳定；  
- **在大模型中的角色**：作为垂直领域高质量语料，用于提升医疗问答、文献摘要等专业任务性能（如 Med-PaLM）。

该数据集与 `datasets/arxiv` 共同代表大模型预训练的**垂直领域知识支柱**。

## 相关页面  
[[datasets/arxiv]]  
[[concepts/medical_nlp]]  
[[concepts/domain_adaptation]]  
[[models/med_palm]]

## 来源  
《百面大模型》，第 2.1 节 “大模型训练开源数据集”，2025 年出版；含 PMC 运营方（NIH/NLM）、规模（500 万）、领域（生物医学）。