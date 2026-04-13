# Common Crawl

_最后更新：2026-04-13_

## 概述  
Common Crawl 是一个自2008年起持续运行的开放网络爬虫项目，提供原始网页快照（HTML）、元数据（WARC headers）及提取文本（WET files），是大模型预训练最核心的**原始语料源**之一；其规模庞大但噪声高，需严格清洗才能用于高质量建模。

## 详细内容  
- **时间跨度与规模**：自2008年启动，截至2023年累计存档超 **250 TB 原始网页数据**（含 > 200B 网页快照），每月新增约 10–15 TB。  
- **数据格式**：以 WARC（Web ARChive）格式存储原始 HTTP 响应；衍生出 WET（plain-text extractions）和 WAT（metadata JSON）文件，便于下游解析。  
- **质量挑战**：  
  - 包含大量低质内容（广告、导航栏、重复模板、机器生成文本、非自然语言代码块）；  
  - 域名分布极度不均衡（Top 0.1% 域名贡献 > 40% 页面）；  
  - 语言混杂（仅约 62% 为英语，中文占比 < 5%，且多为简体无标点片段）。  
- **关键衍生数据集**：  
  - **C4 (Colossal Clean Crawled Corpus)**：源自 *“Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer”*（Raffel et al., JMLR 2020），对 Common Crawl 进行四阶段清洗：  
    1. `HTML → text` 提取（使用 `trafilatura` 类工具，过滤 `<script>`/`<style>`/boilerplate）；  
    2. 启发式过滤（移除含 “copyright”、“lorem ipsum”、“http” 超过3次等模式的文档）；  
    3. 去重（基于 SHA-1 文本哈希 + SimHash 跨文档近似去重）；  
    4. 语言识别（`fasttext` langid，保留置信度 > 0.9 的英文文档）。  
    → 最终 C4 英文子集含 **364M 文档、750GB 文本**，成为 T5、UL2、Flan-T5 等模型基座；在 Llama-2 预训练数据中占比 **15%**。  
- **在 Llama 系列中的实际配比**（Llama-2 Technical Report, Meta 2023）：  
  | 数据源 | 占比 | 备注 |  
  |--------|------|------|  
  | Common Crawl (raw) | — | 未直接使用 |  
  | **C4** | **15%** | 经清洗的英文子集 |  
  | Wikipedia | 4.5% | EN+ZH 双语，经去模板/引用清洗 |  
  | Gutenberg + Books3 | 4% | Gutenberg（经典文学）与 Books3（现代小说/非虚构）混合 |  
  | arXiv | 2.5% | LaTeX → plain text 转换，限 cs.CL / cs.LG / math.ST |  

## 相关页面  
[[datasets/c4]] [[datasets/webtext]] [[models/llama]] [[concepts/data_cleaning]] [[concepts/web_scraping]] [[concepts/language_identification]] [[tools/trafilatura]]

## 来源  
《百面大模型》，第2章“大模型的数据”，第50页（2025）；Llama-2 Technical Report (Meta, 2023)；Raffel et al. "Exploring the Limits of Transfer Learning...", JMLR 2020.