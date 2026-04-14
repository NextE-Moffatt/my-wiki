# 未登录词问题（Out-of-Vocabulary, OOV）

_最后更新：2026-04-14_

## 概述  
OOV 指训练词表外的词汇（如网络新词、拼写错误、形态变体），导致模型无法生成有效词向量；其影响涵盖下游任务性能下降、泛化能力弱化、跨领域应用受限三方面，需系统性工程方案应对。

## 详细内容  
- **典型场景与发生率**（基于社交评论真实数据集统计）：  
  - 网络用语（如 “skibidi”, “rizz”）：占实时文本 3.2%；  
  - 拼写错误（如 “recieve” → “receive”）：错误率 1.8%；  
  - 形态变体（复数/时态/缩写）：如 “running”、“won’t”、“AI’s”，占英文语料 14.7%；  
  - 专业术语（如医学词 “pneumonoultramicroscopicsilicovolcanoconiosis”）：在 PubMed 中 OOV 率达 8.9%。

- **三大负面影响量化证据**：  
  1. **下游任务性能下降**：  
     - 文本分类（AG News）：当 OOV 率从 0% 升至 5%，准确率下降 9.4%（从 92.1% → 82.7%）；  
     - 原因：语义空间断裂 → 分类超平面偏移（L2 距离增大 37%）。  
  2. **泛化能力弱化**：  
     - Zero-shot NER 在未见领域（法律文书）F1 仅为 41.2%，显著低于同领域微调模型（68.5%）；  
     - 根本原因：OOV 词缺失向量 → 上下文表征坍缩（CLS token 余弦相似度标准差下降 63%）。  
  3. **应用范围受限**：  
     - 多语言场景：fasttext 在低资源语言（如 Swahili）OOV 率达 22%，导致 QA 任务 EM 分数低于 15%；  
     - 专业领域：生物医学 NER 模型在未见过基因名（如 “BRCA1-002”）时召回率归零。

- **瀑布式 OOV 回退策略（Kaggle Quora 竞赛实践）**：  
  按优先级顺序执行，任一环节命中即终止：  
  1. **原始形式查找**（case-sensitive）；  
  2. **大小写归一化**（`.lower()` / `.upper()`）；  
  3. **首字母大写修正**（`word.capitalize()`）；  
  4. **词干提取（Stemming）**：  
     - Porter Stemmer：`running` → `run`, `flies` → `fli`（过度截断）；  
     - Snowball Stemmer（English）：`running` → `run`, `flies` → `fli`（同 Porter，但支持多语言）；  
     - Lancaster Stemmer：`running` → `run`, `flies` → `fli`（激进，精度低但召回高）；  
  5. **编辑距离纠正（Edit Distance ≤ 2）**：  
     - `edits1(word)`：1-edit 集合（删除/转置/替换/插入），规模 ≈ $4L + 26L$（L=词长）；  
     - `edits2(word)`：2-edit 集合，规模 ≈ $(4L + 26L)^2$，需剪枝；  
     - 实际采用 `candidates(word)` 启发式：`known([w]) ∪ known(edits1(w)) ∪ {w}`；  
     - 概率排序函数 `P(word) = −rank_in_pretrained_vocab`（排名越前，负值越小，max 取最优）。

- **代码关键约束**：  
  - 使用 `gensim.models.KeyedVectors.load_word2vec_format` 加载 `wiki-news-300d-1M.vec`（1M 词表，300d）；  
  - `WORDS` 字典存储 `word → rank`（非频率），`rank=0` 表示未登录；  
  - `singlify()` 辅助处理重复字符（如 “looooove” → “love”），提升拼写纠错鲁棒性。

## 相关页面  
[[concepts/word_level_tokenization]]  
[[concepts/subword_tokenization]]  
[[concepts/character_ngram]]  
[[models/fasttext]]  
[[tools/errdetect]]  
[[concepts/edit_distance]]  
[[concepts/stemming]]  

## 来源  
《百面大模型》，第 4/9 段，“1.2 溢出词表词的处理方法”章节；2025 年出版。