# BPE（Byte Pair Encoding）

_最后更新：2026-04-13_

## 概述  
BPE 是一种基于贪心合并策略的子词分词算法，通过迭代合并语料中频率最高的相邻子词对构建词表；其核心目标是**最小化编码后序列总长度**，而非建模语言似然。

## 详细内容  

### 算法流程（依据《百面大模型》第34页实现逻辑）  
BPE 训练包含三个关键函数：

1. **`compute_pair_freqs()`**：  
   - 遍历所有 `word → freq` 映射（`self.word_freqs`）；  
   - 对每个词的当前切分 `split = self.splits[word]`（初始为字符级），统计所有相邻子词对 `(split[i], split[i+1])` 的频次；  
   - 忽略单子词（`len(split) == 1`）的词；  
   - 返回 `defaultdict(int)` 形式的 `pair_freqs`。

2. **`merge_pair(a, b)`**：  
   - 对每个词的 `split`，从左到右扫描（`i = 0` 起），**贪心匹配首个 `(a, b)` 相邻对**；  
   - 执行替换：`split[:i] + [a+b] + split[i+2:]`；  
   - **不回溯**，即一次扫描仅合并最左匹配（非全局最优但高效）；  
   - 更新 `self.splits[word]`。

3. **`tokenize(text)`**：  
   - 先经预分词器（如空格/标点分割）得 `pre_tokenized_text`；  
   - 每个预分词再转为字符列表 `[[c for c in word]]`；  
   - 按 `self.merges` 中的合并顺序（从高频到低频）**逐对应用 `merge_pair`**；  
   - 最终 `sum(splits_text, [])` 展平为 token 序列。

### 关键特性（对比 WordPiece）  
| 维度 | BPE | WordPiece |
|------|-----|-----------|
| **合并目标** | 最大化频次（贪心） | 最大化语料似然（EM 算法） |
| **训练目标函数** | 最小化总 token 数（等价于最大化合并收益） | 最大化 $ \log P(\text{corpus} \mid \text{vocab}) $ |
| **词表构建方式** | 自底向上：字符 → 子词 → 常见词缀 | 同样自底向上，但每步选择使似然增益最大的 pair |
| **对 OOV 的鲁棒性** | 高（可分解未登录词为已知子词） | 同等高，但需额外回退逻辑（如 `<unk>`） |

> ⚠️ 矛盾：当前 `pages/concepts/subword_tokenization.md` 未明确区分 BPE 与 WordPiece 的优化目标差异，仅泛称“基于频率”。本页补充具体建模差异。

### 实际影响  
- BPE 在英文中易生成 `ing`, `ed`, `un-`, `re-` 等常见形态素；  
- 中文因字符即语义单元，BPE 常直接保留单字，或合并高频词组（如 `北京`, `人工智能`）；  
- Hugging Face `tokenizers` 库中 `BpeTokenizer` 默认采用此贪心合并逻辑。

## 相关页面  
[[concepts/subword_tokenization]]  
[[concepts/word_level_tokenization]]  
[[concepts/character_ngram]]  
[[models/word2vec]]  
[[models/bert]]  
[[tools/flashattention]]  

## 来源  
《百面大模型》，第34页，“1.3.2 BPE”节；代码片段及算法描述均直接引自原文。