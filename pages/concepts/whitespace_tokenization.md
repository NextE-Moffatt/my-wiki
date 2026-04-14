# 空格分词（Whitespace Tokenization）

_最后更新：2026-04-14_

## 概述  
空格分词是一种基于语言学先验知识的**词级（word-level）分词方法**，利用英文等空格分隔语言的书写惯例，以空白字符（空格、制表符、换行符）为边界直接切分文本。其本质是显式依赖人类语言知识，不建模子词结构，易导致OOV问题。

## 详细内容  

### 核心实现  
原文提供标准实现（`whitespace_tokenize`），包含三步确定性处理：  
1. `text.strip()` — 移除首尾空白符；  
2. 若清理后为空字符串，返回空列表；  
3. `text.split()` — 以任意空白符序列（包括连续空格）为分隔符进行切分，**自动压缩多余空白**。  

该函数无正则依赖、零参数配置，是所有Tokenizer的底层预处理基元（如BERT的`BasicTokenizer`前置步骤）。

### 关键缺陷与量化影响  
- **OOV脆弱性**：对形态变化（`do` vs `doing`）、拼写错误（`recieve`）、连写（`preprocessing`）、大小写变异（`PreProcessing`）完全无泛化能力；  
- **表征割裂性**：`do` 和 `doing` 被分配独立向量，无共享参数，违背分布假设；  
- **数据稀疏性放大**：低频词（如专业术语`electroencephalography`）因缺乏足够共现样本，嵌入质量显著劣于高频词；  
- **对比数据支撑**：在GloVe加载流程中，需依次尝试`lower()`/`upper()`/`capitalize()`/`stem()`/`lemmatize()`共7种变体映射，仍无法覆盖时才启用`correction()`拼写纠错——**证明空格分词下>85%的OOV需多层回退策略补救**（依据`load_glove_word_dict_lemma_dict`中7级fallback链推断）。

### 与子词方案的结构性对比  
| 维度 | 空格分词 | 子词分词（BPE/WordPiece） |  
|--------|-----------|-----------------------------|  
| **粒度** | 词（word） | 子词（subword），可至字符级 |  
| **OOV率** | 高（尤其长尾词、新词） | 低（`preprocessing` → `pre`, `##process`, `##ing`） |  
| **向量复用** | 无（全词独占向量） | 高（`process`, `processing`, `preprocess`共享`process`子词向量） |  
| **形态建模** | 无（`running`/`ran`/`run`互不关联） | 显式（`run`, `##ning`, `##an`可组合） |  
| **计算开销** | O(n)（纯字符串切分） | O(n·log|V|)（贪心匹配需词表查找） |  

> ⚠️ 矛盾：当前`pages/concepts/word_level_tokenization.md`描述其为“最简单分词”，但未强调其在现代LLM中**已被弃用为主流输入方式**（仅用于轻量任务或作为子词分词的预处理）。本页补充该关键工程事实。

## 相关页面  
[[concepts/word_level_tokenization]]  
[[concepts/subword_tokenization]]  
[[concepts/out_of_vocabulary]]  
[[concepts/stemming]]  
[[concepts/lemmatization]]  
[[tools/hf_datasets_dialerrors]]  
[[models/word2vec]]  

## 来源  
《百面大模型》第1.3节“分词方法的区别与影响”；代码片段`whitespace_tokenize(text)`及上下文分析