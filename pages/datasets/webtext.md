# WebText

_最后更新：2026-04-14_

## 概述  
WebText 是 OpenAI 构建的高质量网页文本数据集，通过 Reddit 出站链接的社交信号（≥3 个赞）筛选优质内容，旨在解决 Common Crawl 数据质量低的问题；虽未在 Llama 配比中出现，但被明确列为大模型预训练重要数据源。

## 详细内容  
根据《百面大模型》第 2.1 节，WebText 的核心设计如下：

- **构建动机**：Common Crawl 数据量巨大但噪声高，WebText 提出“**社交质量代理**”（social quality proxy）——以 Reddit 用户投票（upvote ≥3）作为网页内容质量的间接指标；  
- **构建流程**：  
  - 抓取 Reddit 所有出站链接；  
  - 仅保留获 ≥3 个赞的链接对应网页；  
  - 下载并提取纯文本（移除 HTML、JS、广告）；  
- **规模与影响**：  
  - WebText-v1（2019）：约 40GB 文本（约 8B tokens）；  
  - WebText-2（2020）：扩展至 60GB；  
  - 是 GPT-2 训练的核心语料，直接促成其 zero-shot 能力突破；  
- **与 C4 的哲学差异**：  
  - C4：规则驱动清洗（entropy, n-gram dedup）；  
  - WebText：人本驱动筛选（crowdsourced quality signal）；  
- **局限性**：文化偏向（Reddit 用户以英语母语者为主）、主题偏向（科技、游戏、亚文化内容集中）。

该数据集是 `concepts/data_quality_proxy` 页面的标杆案例。

## 相关页面  
[[datasets/common_crawl]]  
[[datasets/c4]]  
[[concepts/data_quality_proxy]]  
[[models/gpt]]  
[[concepts/social_signal_in_data]]

## 来源  
《百面大模型》，第 2.1 节 “大模型训练开源数据集”，2025 年出版；含 WebText 构建方（OpenAI）、筛选逻辑（Reddit ≥3 赞）、核心目标（解决 Common Crawl 质量问题）。