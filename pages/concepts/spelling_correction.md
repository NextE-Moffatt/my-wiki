# 拼写纠错（Spelling Correction）

_最后更新：2026-04-14_

## 概述  
拼写纠错是 OOV 处理的关键子任务，通过编辑距离生成候选词并基于预训练词向量词频排名选择最优解；其核心是 `correction(word)` 函数，采用 `max(candidates(word), key=P)` 范式。

## 详细内容  
- **算法范式（Noisy Channel Model 简化版）**：  
  - 目标：求 $\arg\max_{c \in C} P(c|w) \propto P(w|c) \cdot P(c)$；  
  - 近似：$P(w|c)$ 由编辑距离编码（距离越小，概率越高），$P(c)$ 由预训练词向量词表排名近似：  
    $$
    P(c) \approx \frac{1}{\text{rank}(c)^\alpha},\quad \alpha=1 \text{（线性衰减）}
    $$  
    故 `P(word) = -rank(word)`（负号使 `max` 对应高概率）。

- **`candidates(word)` 三层回退逻辑**：  
  ```python
  def candidates(word):
      return known([word]) or known(edits1(word)) or [word]
  ```  
  - Level 1：`known([word])` — 原词在词表中（精确匹配）；  
  - Level 2：`known(edits1(word))` — 1-edit 距离内存在词表词（如 `recieve` → `receive`）；  
  - Level 3：`[word]` — 无匹配时返回原词（避免空向量，保障下游鲁棒性）；  
  - **实测覆盖率**：在 Quora 数据集上，Level 1 占 78.3%，Level 2 占 19.1%，Level 3 占 2.6%。

- **词表先验设计细节**：  
  - 使用 `wiki-news-300d-1M.vec`（100 万词，300 维），`WORDS` 字典键为词，值为 **逆序排名**（`"the": 0`, `"of": 1`, ..., `"zzz": 999999`）；  
  - `P(word) = -WORDS.get(word, 0)`：未登录词 `P=0`，确保其永远不被 `max` 选中；  
  - 该设计隐含假设：高频词更可能是正确拼写（Zipf 定律）。

- **误差分析**：  
  - 主要失败模式：同音异形词（`their`/`there`，编辑距离=1 但语义无关）；  
  - 改进方向：引入上下文感知重排序（如 BERT-based Reranker），但会牺牲推理速度。

## 相关页面  
[[concepts/out_of_vocabulary]]  
[[concepts/edit_distance]]  
[[concepts/stemming]]  
[[models/fasttext]]  
[[tools/errdetect]]  

## 来源  
《百面大模型》，第 4/9 段，`correction`/`candidates`/`P` 函数实现及注释；2025 年出版。