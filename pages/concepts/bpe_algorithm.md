# BPE 算法

_最后更新：2026-04-14_

## 概述  
Byte Pair Encoding（BPE）是一种**频率驱动**的贪心子词合并算法，通过迭代合并语料中出现频次最高的相邻字符/子词对，构建紧凑且泛化性强的子词词表；其分词过程为确定性自左向右合并，无需概率建模。

## 详细内容  

### 训练流程（精确算法描述）  
设初始词频统计 `word_freqs: {word → count}`，初始分割 `splits: {word → [char₁, char₂, …]}`，词汇表 `vocab = ["</w>"] + alphabet`（`</w>` 为词尾标记）：  

1. **计算对频次**（`compute_pair_freqs`）：  
   对每个词 `w` 及其当前分割 `splits[w] = [s₁,s₂,…,sₖ]`，遍历所有相邻对 `(sᵢ, sᵢ₊₁)`，累加 `word_freqs[w]` 到 `pair_freqs[(sᵢ,sᵢ₊₁)]`；  

2. **选取最优对**：  
   找出 `argmax_{pair} pair_freqs[pair]`，记为 `(a,b)`；  

3. **执行合并**（`merge_pair`）：  
   对每个词 `w`，将其 `splits[w]` 中所有连续 `(a,b)` 替换为 `a+b`（注意：**仅合并一次/位置**，非全局替换）；  
   更新 `vocab ← vocab ∪ {a+b}`；  
   更新 `merges[(a,b)] = a+b`；  

4. **终止条件**：`len(vocab) ≥ vocab_size`。  

> ✅ 示例：`["low", "lowest", "new", "widest"]` 频次均为 1 → 初始对频次：`("l","o")=2`, `("o","w")=3`, `("e","s")=2`, `("s","t")=3` → 首轮合并 `("o","w")→"ow"`；后续 `"low"` → `["l","ow"]`, `"lowest"` → `["l","ow","e","s","t"]`。

### 分词流程（Deterministic Left-to-Right Merge）  
给定训练好的 `merges` 映射（按合并顺序排序），对输入文本：  
- 预分词为单词（如 `"I am not happy"` → `["I","am","not","happy"]`）；  
- 每个单词拆为字符列表（`"happy"` → `["h","a","p","p","y"]`）；  
- **按 `merges` 顺序依次应用**：对每个 `(a,b)→ab`，扫描字符列表，将所有 `a,b` 连续对替换为 `ab`；  
- 最终拼接所有子词列表为 token 序列。  

> ⚠️ 关键细节：BPE 分词**不回溯**，合并顺序决定结果（如先合 `"pp"` 再合 `"hap"` vs 反之，结果不同）；因此 `merges` 必须按频次降序存储。

### 复杂度与工程特性  
- 时间复杂度：训练为 $O(|C| \cdot L \cdot I)$，其中 $|C|$ 为语料词数，$L$ 为平均词长，$I$ 为迭代轮数；  
- 空间优化：实际实现（如 `tokenizers` 库）使用**Trie 结构缓存所有可能子词路径**，分词时 $O(L)$ 查找；  
- `</w>` 标记作用：显式区分词内/词尾子词（如 `"playing"` → `["play","ing</w>"]`），缓解形态歧义。

## 相关页面  
[[concepts/bpe]]  
[[concepts/wordpiece_algorithm]]  
[[concepts/subword_tokenization]]  
[[concepts/frequency_driven_merge]]  
[[models/gpt]]  
[[models/gpt2]]  
[[tools/tokenizers]]

## 来源  
《百面大模型》第 6/9 段（2025）；Sennrich et al., ACL 2016（BPE 原始论文）