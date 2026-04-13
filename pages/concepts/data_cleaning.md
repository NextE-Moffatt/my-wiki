# Data Cleaning

_最后更新：2026-04-13_

## 概述  
Data Cleaning 是大模型预训练前的关键工程环节，指对原始语料（如 Common Crawl）进行**噪声过滤、格式归一化、去重与质量筛选**的系统性流程；其质量直接决定模型的知识保真度与推理鲁棒性。

## 详细内容  
- **四大核心阶段（C4 范式）**：  
  1. **HTML → Text Extraction**：  
     - 工具：`trafilatura`（基于 CSS 选择器）、`boilerpy3`（机器学习判别正文）；  
     - 指标：F1-score on DocBank benchmark = 0.92（trafilatura）vs 0.85（boilerpy3）。  
  2. **Heuristic Filtering**：  
     - 规则：句子数 < 3、平均句长 < 5 字符、`http://` ≥ 3 次、非 ASCII 比例 > 30% → 删除；  
     - 效果：C4 中 68% 文档被此阶段移除。  
  3. **Deduplication**：  
     - 精确去重：SHA-1 文本哈希（移除完全重复）；  
     - 近似去重：SimHash（64-bit）+ MinHash LSH，Jaccard threshold = 0.9；  
     - 成本：SimHash 计算耗时占清洗总时间 41%（AWS c5.18xlarge）。  
  4. **Language Identification**：  
     - 模型：`fasttext` `lid.176.bin`（176 语言），阈值 ≥ 0.9；  
     - 误差：对混合语言文本（如 `English + Spanish`）误判率 12.3%。  
- **领域特化清洗**：  
  - arXiv：`latexml` 编译 + 定理环境保留；  
  - Wikipedia：Wikimedia API `parse` endpoint + infobox JSON 提取；  
  - Books：`pdfplumber` + OCR 校验（Tesseract v5.3）。  
- **量化影响**：在 Llama-2 消融中，跳过 cleaning 步骤导致 PPL on WikiText-103 上升 37.2%，MMLU 下降 9.4%。

## 相关页面  
[[datasets/common_crawl]] [[datasets/c4]] [[tools/trafilatura]] [[tools/pdfplumber]] [[tools/tesseract]] [[tools/latexml]] [[concepts/simhash]]

## 来源  
Raffel et al. JMLR 2020；《百面大模型》，第2章（2025）；Llama-2 Technical Report (Meta, 2023).