# 编辑距离（Edit Distance）

_最后更新：2026-04-14_

## 概述  
编辑距离（Levenshtein 距离）是衡量两字符串差异的最小单字符编辑操作数（插入、删除、替换），在 OOV 拼写纠错中作为核心相似性度量，其高效实现支撑 `edits1`/`edits2` 候选生成。

## 详细内容  
- **定义与计算**：  
  - 字符串 $s$ 到 $t$ 的 Levenshtein 距离 $d(s,t)$ 是使 $s=t$ 所需的最少操作数；  
  - 动态规划递推式：  
    $$
    d(i,j) = 
    \begin{cases}
    j & \text{if } i = 0 \\
    i & \text{if } j = 0 \\
    d(i-1,j-1) & \text{if } s[i] = t[j] \\
    1 + \min\big(d(i-1,j), d(i,j-1), d(i-1,j-1)\big) & \text{otherwise}
    \end{cases}
    $$  
  - 时间复杂度 $O(|s|\cdot|t|)$，空间优化至 $O(\min(|s|,|t|))$。

- **在 OOV 纠错中的工程实现**（《百面大模型》代码节选）：  
  - `edits1(word)`：生成所有 1-edit 距离字符串集合，规模为：  
    - 删除：$L$ 个（`word[:i] + word[i+1:]`）；  
    - 转置：$L-1$ 个（`word[:i] + word[i+1] + word[i] + word[i+2:]`）；  
    - 替换：$26L$ 个（每个位置替换为 a–z）；  
    - 插入：$26(L+1)$ 个；  
    - **总计**：$4L + 26L = 30L$（$L$=词长），对 `apple`（L=5）生成 150 个候选。  
  - `edits2(word)`：对 `edits1(word)` 中每个结果再调用 `edits1`，规模呈平方爆炸，故实际采用 `candidates(word)` 启发式：仅探索 `edits1` 层并 fallback 到原始词。

- **性能瓶颈与优化**：  
  - 暴力生成 `edits2` 对长词（L>10）不可行（`edits1(apple)=150`, `edits2(apple)≈22,500`）；  
  - 工程实践：限定 `edits1` 结果中仅保留 `known(...)` 子集（查预训练词表），再按 `P(word)` 排序取 Top-1；  
  - `P(word) = -rank_in_pretrained_vocab`：利用词频排名先验，避免低频词干扰（如 `qzx` 距离 `quiz` 为 2，但 `qzx` 不在词表中，`P(qzx)=0`）。

## 相关页面  
[[concepts/out_of_vocabulary]]  
[[concepts/spelling_correction]]  
[[models/fasttext]]  
[[tools/errdetect]]  

## 来源  
《百面大模型》，第 4/9 段，`edits1`/`edits2`/`correction` 函数定义及注释；2025 年出版。