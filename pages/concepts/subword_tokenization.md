# 子词分词（Subword Tokenization）

_最后更新：2026-04-13_

## 概述  
子词分词是一种将单词切分为语义/形态上有意义的子单元（如词根、词缀、字符n-gram）的文本预处理技术，核心目标是缓解OOV（Out-of-Vocabulary）问题，同时在表征粒度上平衡泛化性与特异性。

## 详细内容  

### 1. 设计动机与核心优势  
- **OOV缓解机制**：当遇到未登录词（如 `preprocessing`），不直接映射为 `[UNK]`，而是将其分解为子词序列（如 `pre-`、`process`、`-ing`），再通过聚合（默认为向量平均或求和）生成最终嵌入。因共享子词（如 `process` 出现在 `processor`, `reprocess` 中），训练数据更充分，嵌入质量更高。  
- **形态建模能力**：可显式捕获屈折变化（如 `do` → `doing`）、派生关系（`un-`, `-able`）及跨语言构词共性（如英语中26+26个字母可组合任意词）。  
- **稠密表征 vs 稀疏表征**：相比空格分词（word-level），子词分词使向量空间更稠密——`do` 和 `doing` 共享 `do` 子词向量，语义相似性得以保留；而空格分词下二者向量正交，无法建模词形关联。

### 2. 主流算法原理对比  

| 维度 | WordPiece | Byte Pair Encoding (BPE) | Unigram |
|--------|------------|---------------------------|----------|
| **合并目标** | 最大化语料似然：合并 `s_i, t_i` 后使 `Δlog P(S) = log P(c_i) − [log P(s_i) + log P(t_i)]` 增益最大 | 最大化相邻单元对频次：每次合并语料中出现频率最高的字符/子词对 | 最小化负对数似然（基于隐马尔可夫假设） |
| **初始化** | 将所有词拆为最小单元（字符级） | 字符级基础词表（含 `</w>` 边界标记） | 预设大词表（如50k），通过EM算法迭代剪枝 |
| **分词策略** | 贪心最长匹配（Longest Match First）：对 `unaffable` 输出 `["un", "##aff", "##able"]`（`##` 表示非首子词） | 自底向上合并，分词时从长到短尝试匹配（如 `lowers` → `low` + `ers`，而非 `lower` + `s`） | 基于概率的Viterbi解码，返回最高概率路径 |

> ⚠️ 矛盾：原文称WordPiece“以似然提升为合并目标”，但标准文献（Wu et al., 2016）指出其实际采用**似然近似下的贪心合并**（即最大化 `P(merge) ≈ count(merge)/∑count(all pairs)`），并非严格优化 `log P(S)`。此差异需后续交叉验证。

### 3. 实现细节（关键代码逻辑）  
- **WordPiece分词器核心逻辑**（`WordpieceTokenizer.tokenize`）：  
  - 对每个token执行贪心最长前缀匹配；  
  - 若匹配失败且字符数 ≤ `max_input_chars_per_word`（默认100），则标记为 `[UNK]`；  
  - 子词拼接使用 `##` 前缀标识非首子词（如 `##able`），确保位置感知。  
- **BPE训练循环**（`BPE.train`）：  
  - 步骤1：统计词频 `word_freqs`；  
  - 步骤2：构建初始字符词表 `vocab = ["</w>"] + sorted(alphabet)`；  
  - 步骤3：对每个词 `split[word] = list(char)`；  
  - 步骤4：迭代 `compute_pair_freqs()` → 找最高频对 `best_pair` → `merge_pair()` → 更新 `vocab`，直至 `len(vocab) == vocab_size`。  
  - `compute_pair_freqs()` 计算频次时加权：`pair_freqs[(a,b)] += freq(word)`（非简单计数，体现词频重要性）。

### 4. 大模型时代演进  
- BERT、RoBERTa、T5等主流PLM均采用WordPiece（BERT）或BPE（GPT-2/3）；  
- Llama系列使用SentencePiece（Unigram变体），支持更鲁棒的未知词切分；  
- 当代分词器（如LLaMA-3的`llama-tokenizer`）进一步融合**词组感知**（phrase-aware merging）与**多语言统一编码**（如将中文字符、日文假名、拉丁字母同置一空间）。

## 相关页面  
[[concepts/out_of_vocabulary]]  
[[concepts/tokenization]]  
[[concepts/soft_clustering]]（子词聚类可视作软约束的语义聚类）  
[[models/bert]]（使用WordPiece）  
[[models/gpt]]（GPT-2/3使用BPE）  
[[models/llama]]  
[[tools/hf_datasets_dialerrors]]（依赖子词对齐进行错误定位）  
[[concepts/distributional_hypothesis]]（子词共享强化了“共现即语义”假设）

## 来源  
《百面大模型》第1章第1.3节 “分词方法的区别与影响”，pp.29–33；原始PDF段落（第5/9段）