# PubMed Central

_最后更新：2026-04-13_

## 概述  
PubMed Central（PMC）是由美国国立卫生研究院（NIH）运营的免费全文生物医学文献库，收录约500万份经同行评审的期刊论文，是大模型**专业领域对齐（Domain Alignment）与生命科学推理**的核心语料。

## 详细内容  
- **数据构成**：  
  - 开放获取（OA）论文占比 78%（2023），其余需机构订阅；  
  - 学科覆盖：生物医学（62%）、临床医学（23%）、药学（9%）、公共卫生（6%）；  
  - 结构化元数据：MeSH（Medical Subject Headings）标签、PMID、DOI、基金号（NIH Grant ID）。  
- **文本处理关键技术**：  
  - XML 解析：使用 `NLM DTD` schema 提取 `<abstract>`/`<introduction>`/`<methods>`/`<results>`/`<discussion>`；  
  - 术语标准化：`MetaMap` 工具将自由文本映射至 UMLS（Unified Medical Language System）概念ID；  
  - 公式处理：保留 `<inline-formula>` 和 `<disp-formula>` 的 MathML 表示。  
- **在 Llama-2 中的角色**：未被直接使用（Llama-2 技术报告未列 PMC），但作为 **BioMedLM / Galactica 等专业模型的主干语料**；其缺失解释了 Llama-2 在 `MedQA-USMLE` 基准上仅得 42.3%（vs Galactica 68.1%）。  
- **与 arXiv 对比**：  
  | 维度 | arXiv | PubMed Central |  
  |------|-------|----------------|  
  | 审稿状态 | 预印本（无审稿） | 同行评审（Peer-reviewed） |  
  | 公式密度 | 12.7 公式/千字 | 8.3 公式/千字 |  
  | 术语规范性 | 高（LaTeX 定义） | 极高（UMLS + SNOMED CT） |  
  | 中文支持 | 无 | 有（CNKI PMC Mirror，但未入主流训练） |

## 相关页面  
[[datasets/arxiv]] [[models/galactica]] [[concepts/domain_adaptation]] [[tools/metamap]] [[concepts/umls]]

## 来源  
《百面大模型》，第2章，第50页（2025）；PMC Annual Report (NIH, 2023)；Galactica Paper (Meta, 2022).