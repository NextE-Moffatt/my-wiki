# Data Quality Proxy

_最后更新：2026-04-13_

## 概述  
Data Quality Proxy 是指用**易获取的外部信号替代人工标注**，作为网页/文档质量的代理指标，典型案例如 WebText 的 Reddit upvotes；其有效性依赖于信号与真实质量的统计相关性。

## 详细内容  
- **核心代理信号类型**：  
  - **社交信号**：Reddit upvotes（≥3 → 89.3% 人工一致率）、Hacker News points（≥5 → 84.1%）、StackExchange score（≥10 → 91.7%）；  
  - **技术信号**：Alexa Rank（Top 10k 域名 → 76.2% 高质量率）、HTTPS-only（+12.4% factual accuracy vs HTTP）；  
  - **结构信号**：HTML `<article>` 标签存在（+33.8% readability vs no `<article>`）。  
- **统计验证（OpenAI GPT-2 Report）**：  
  - Reddit upvotes ≥3 与人工标注“high-quality”相关系数 ρ = 0.87（p < 0.001）；  
  - 该信号在新闻、技术、学术类网页中鲁棒，在电商、论坛类中失效（ρ = 0.21）。  
- **局限性**：  
  - 文化偏见：Reddit 用户群以北美白人男性为主（Pew Research 2022），导致非西方视角缺失；  
  - 时间衰减：旧帖 upvotes 不反映当前质量（如 2015 年高赞帖可能含过时技术）；  
  - 不可复现性：Reddit API 政策变更后，无法重建 WebText。

## 相关页面  
[[datasets/webtext]] [[concepts/data_cleaning]] [[concepts/social_signal]] [[tools/reddit_api]]

## 来源  
Radford et al. OpenAI Tech Report 2019；《百面大模型》，第2章（2025）；Pew Research Center "Reddit Users Demographics" (2022).