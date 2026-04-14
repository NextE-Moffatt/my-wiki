# 词干提取（Stemming）

_最后更新：2026-04-14_

## 概述  
词干提取是将词汇还原为其词干（stem）的启发式规则过程，用于缓解 OOV 问题；主流算法包括 Porter、Snowball 和 Lancaster，三者在激进程度、精度与召回上存在明确 tradeoff。

## 详细内容  
- **定义与目标**：  
  - 词干（stem）：词汇的语法核心部分（如 `running` → `run`, `better` → `bet`），**不保证是合法单词**；  
  - 区别于词形还原（lemmatization）：后者依赖词性标注与词典（如 `better` → `good`），计算开销高但语义保真度强。

- **三大算法对比（基于 NLTK 实现）**：  
  | 算法 | 规则特点 | 示例 | 精度 | 召回 | 适用场景 |  
  |------|----------|------|------|------|----------|  
  | **Porter** | 5 阶段后缀剥离（如 `-ed`, `-ing`, `-s`），保守 | `caresses` → `caress`, `ponies` → `poni` | 84.2% | 71.5% | 通用文本、检索系统 |  
  | **Snowball** | Porter 的国际化扩展（支持 15+ 语言），英语版等价 | `caresses` → `caress`, `ponies` → `poni` | 83.9% | 72.1% | 多语言 OOV 回退 |  
  | **Lancaster** | 迭代式强规则（如 `-ed` → 删除，`-ing` → 删除），激进 | `caresses` → `caress`, `ponies` → `poni`, `running` → `run` | 76.3% | 89.6% | 高召回需求（如拼写纠错候选生成） |  

- **在 OOV 处理中的实证效果**（Quora Insincere Questions 数据集）：  
  - 单独使用 Porter：OOV 解决率 42.7%；  
  - Porter + Snowball + Lancaster 三级并行：解决率提升至 63.1%（+20.4pp）；  
  - 但引入 5.8% 错误归一化（如 `global` → `glob`），需配合 `P(word)` 排序过滤。

- **技术限制**：  
  - 无法处理不规则变化（`went` → `go`, `mice` → `mouse`）；  
  - 对派生词无效（`happiness` → `happi`，丢失语义）；  
  - 在子词模型（BPE/WordPiece）中已基本被取代，但在 fasttext 和传统检索系统中仍为核心组件。

## 相关页面  
[[concepts/out_of_vocabulary]]  
[[concepts/word_level_tokenization]]  
[[models/fasttext]]  
[[concepts/subword_tokenization]]  
[[concepts/lemmatization]]  

## 来源  
《百面大模型》，第 4/9 段，“1.2 溢出词表词的处理方法”章节中 `PorterStemmer`/`SnowballStemmer`/`LancasterStemmer` 实现细节；2025 年出版。