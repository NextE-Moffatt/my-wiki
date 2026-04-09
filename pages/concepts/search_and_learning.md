# 搜索与学习（Search and Learning）

_最后更新：2026-04-10_

## 概述

Rich Sutton 在 The Bitter Lesson 中指出，搜索和学习是 AI 中唯二能随算力无限扩展的技术类别，是通用方法力量的核心体现。

## 详细内容

### 搜索（Search）

在解空间中系统性地探索，随算力增加可搜索更深/更广。
- 代表：深度优先/广度优先搜索、MCTS（蒙特卡洛树搜索）、beam search
- 案例：深蓝（1997）、AlphaGo 的 MCTS

### 学习（Learning）

从数据中自动提取模式，随数据量和模型规模扩展持续改善。
- 代表：反向传播、深度学习、Transformer、LLM 预训练
- 案例：语音识别（HMM → 深度学习）、ImageNet → ViT、GPT 系列

### 二者的共同特质

- 不依赖人类对具体领域的先验知识
- 性能随算力近乎单调提升
- 发现的规律可超越人类显式理解的范畴

### 与人类知识方法的对比

| | 搜索/学习 | 人类知识方法 |
|---|---|---|
| 短期效果 | 较弱 | 较强 |
| 长期扩展 | 无上限 | 触顶 |
| 可解释性 | 低 | 高 |
| 研究满足感 | 低（"暴力"） | 高（"优雅"） |

## 相关页面

- [[bitter_lesson]] — 提出此分类的原始文章
- [[scaling_computation]] — 算力扩展背景
- [[human_knowledge_vs_computation]] — 历史对比

## 来源

- Rich Sutton, "The Bitter Lesson", 2019
