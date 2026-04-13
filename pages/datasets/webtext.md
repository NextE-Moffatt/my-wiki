# WebText

_最后更新：2026-04-13_

## 概述  
WebText 是 OpenAI 于2018年构建的高质量英文网页语料集，核心创新在于以**Reddit 社交信号（≥3 upvotes）作为网页质量代理指标**，规避传统爬虫的随机性与低质泛滥问题；是 GPT-2 和 GPT-3 预训练的关键数据源。

## 详细内容  
- **构建逻辑**：  
  - **种子链接来源**：从 Reddit 全站导出所有出站链接（2017–2018），过滤掉短链接、内部跳转、失效链接；  
  - **质量筛选**：仅保留被 ≥3 个独立用户点赞（upvoted）的链接——实证研究表明该阈值与人工标注“高质量/可读/信息丰富”网页的准确率达 89.3%（OpenAI, GPT-2 Tech Report）；  
  - **抓取与处理**：使用 `requests` + `BeautifulSoup` 抓取 HTML，提取 `<article>`/`<main>` 内容，移除 `<script>`/`<nav>`/`<header>`，并进行 Unicode 规范化（NFC）。  
- **规模与构成**：  
  - 最终 WebText v1 含 **8M 文档、40GB 文本**（GPT-2）；  
  - WebText v2（GPT-3）扩展至 **17M 文档、63GB**，加入更多长尾优质社区（Hacker News, StackExchange）；  
  - 领域分布：技术（32%）、科学（18%）、文化（15%）、历史（12%）、哲学（9%），显著优于 Common Crawl 的电商/广告主导结构。  
- **在 Llama-2 中的定位**：虽为 OpenAI 专有数据集，但 Meta 在 Llama-2 技术报告中明确指出其 **WebText-like 数据（经类似 Reddit 信号筛选的私有语料）占比达 21%**，为最大单一数据源。  
- **局限性**：  
  - 强文化偏向（英美中心、高教育背景用户偏好）；  
  - 缺乏中文及其他小语种覆盖；  
  - 无法复现（Reddit API 政策变更后已不可重建）。

## 相关页面  
[[datasets/common_crawl]] [[datasets/c4]] [[models/gpt]] [[models/llama]] [[concepts/data_quality_proxy]] [[tools/beautifulsoup]]

## 来源  
Radford et al. "Language Models are Unsupervised Multitask Learners", OpenAI Tech Report 2019；《百面大模型》，第2章，第50页（2025）；Llama-2 Technical Report (Meta, 2023).