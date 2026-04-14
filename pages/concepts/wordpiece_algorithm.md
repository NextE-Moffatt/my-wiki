# WordPiece 算法

_最后更新：2026-04-14_

## 概述  
WordPiece 是一种基于**最大似然估计**的子词分词算法，通过贪心地合并能最大化语料库概率的相邻子词对来构建词汇表；其分词阶段采用**贪婪最长匹配（Greedy Longest Match）**策略，并引入 `#` 前缀标记子词边界。

## 详细内容  

### 训练目标与建模本质  
WordPiece 的核心训练目标是：在给定当前词汇表 $V_t$ 下，最大化语料库 $C$ 的对数似然  
$$
\mathcal{L}(V_t) = \sum_{w \in C} \log P(w \mid V_t)
$$  
其中单词 $w$ 的概率由其最优子词分解路径决定：  
$$
P(w \mid V_t) = \max_{(s_1,\dots,s_k) \in \text{Segmentations}(w)} \prod_{i=1}^k P(s_i)
$$  
该优化通过**EM-style 迭代**实现：固定分割方式估计子词概率 → 固定子词概率重选最优分割 → 合并提升似然的相邻对（如 `"aff"+"able" → "affable"` 若使 $\log P$ 增益最大）。

### 分词算法（Greedy Longest Match）  
输入文本经 `BasicTokenizer`（空格+标点预处理）后，对每个 token 执行：  
1. 若 token 长度 > `max_input_chars_per_word`（默认 200），直接替换为 `[UNK]`；  
2. 否则从左至右扫描字符序列 `chars = [c₁,c₂,…,cₙ]`，对每个起始位置 `start`，尝试从最长可能子串 `chars[start:end]`（`end` 从 `len(chars)` 递减）匹配词表；  
3. 若 `start > 0`，则前缀加 `#`（如 `"affable"` 中第二段 `"ffable"` → `"#ffable"`），确保子词可逆重构；  
4. 匹配成功则切分并推进 `start = end`；失败则整 token 标记为 `[UNK]`。  

> ✅ 示例：`"unaffable"` → `["un", "#aff", "#able"]`  
> ⚠️ 注意：`"#aff"` 和 `"#able"` 仅在非首段出现，保证 `"un"+"#aff"+"#able"` 可无歧义还原为 `"unaffable"`。

### 与 BPE 的关键区别  
| 维度 | WordPiece | BPE |
|------|-----------|-----|
| **合并准则** | 最大化语料似然（概率驱动） | 最大化相邻单元对频次（频率驱动） |
| **分词策略** | 贪心最长匹配（动态回溯式） | 贪心最短匹配（自左向右逐字符合并） |
| **边界标记** | 使用 `#` 前缀区分非首段子词 | 无显式边界标记，依赖词表原子性 |
| **未登录词处理** | 降级为字符级切分 + `#` 标记 | 降级为字符级切分（无 `#`） |

### 实现约束与鲁棒性  
- `max_input_chars_per_word` 是硬截断阈值，防止 OOV token 导致无限循环；  
- `#` 前缀机制使 WordPiece 具备**显式子词边界感知能力**，显著提升下游任务（如 NER、形态分析）的边界识别精度；  
- 在中文场景中，因汉字本身即语义单元，WordPiece 常退化为单字分词，但 `#` 标记仍用于复合词（如 `"#上海"` 表示“上海”作为后缀）。

## 相关页面  
[[concepts/wordpiece]]  
[[concepts/bpe]]  
[[concepts/subword_tokenization]]  
[[concepts/greedy_longest_match]]  
[[concepts/out_of_vocabulary]]  
[[models/bert]]  
[[models/roberta]]

## 来源  
《百面大模型》第 6/9 段（2025）；BERT 原论文（Devlin et al., NAACL 2019）附录 A