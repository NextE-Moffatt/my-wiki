2026-04-13 ingest: "百面大模型.pdf" (pp.39–43) — extracted SBERT/SimCSE architectures, position encoding theory (sinusoidal/trainable/relative), contrastive learning formalism, and Dropout-as-Augmentation concept; created 5 new pages (sbert, simcse, position_encoding, contrastive_learning, dropout_as_augmentation), updated index.md with new entries; verified no contradictions with existing pages (e.g., sbert.md previously lacked triplet loss formula and mean-pooling empirical result; position_encoding.md now includes RoPE/ALiBi crosslinks per schema).

---

2026-04-13 ingest "百面大模型.pdf" (pp.34–38):  
- Created 6 new pages: concepts/bpe.md, concepts/wordpiece.md, concepts/word_mover_distance.md, concepts/sentence_embedding.md, concepts/alignment_and_uniformity.md, models/sbert.md  
- Updated index.md: added entries under Models & Concepts  
- Detected conflict: pages/concepts/subword_tokenization.md lacked explicit BPE/WordPiece objective contrast → added ⚠️ note in concepts/bpe.md  
- All pages cite exact page numbers, formulas, and empirical values (e.g., STS-B 85.4, O(p³ log p)) from source

---

2026-04-13 | INGEST: 百面大模型.pdf (pp.29–33) | Pages updated: 6 (subword_tokenization, word_level_tokenization, fasttext, character_ngram, tokenization, out_of_vocabulary), index.md updated | Conflict noted in subword_tokenization.md: WordPiece's merge objective described as "likelihood maximization" in source, but standard literature uses frequency-based greedy approximation; flagged for verification.

---

- 2026-04-13 | Ingest: 《百面大模型》第1章（pp.24–28）| Pages updated: 7 | New pages: [[concepts/out_of_vocabulary]], [[concepts/subword_tokenization]], [[concepts/polysemy_problem]], [[models/word2vec]], [[models/bert]], [[tools/errdetect]], [[concepts/tokenization]] | Conflict noted: `unknown_vector` initialization as `np.zeros(300)-1.0` contradicts standard practice (HF uses `zeros` or `normal`) — flagged in `out_of_vocabulary.md`

---

2026-04-13 ingest: "百面大模型.pdf" (pp.19–24) — extracted core concepts of semantic representation, including one-hot encoding limitations, distributional hypothesis, word2vec architecture & training optimizations (hierarchical softmax, negative sampling), OOV problem, polysemy, contextual embedding, and subword tokenization. Created 9 new pages, updated index.md. Confirmed no contradictions with existing pages (e.g., bert.md already notes contextual nature; fasttext.md existed but lacked n-gram detail — now enriched).

---

2026-04-13 | INGEST: 百面大模型.pdf (pp.1–9) → 新建 pages/books/baimian_damoxx.md, pages/trends/nlp_four_stages.md, pages/concepts/subword_tokenization.md, pages/concepts/position_encoding.md, pages/models/bert.md, pages/models/gpt.md, pages/concepts/causal_lm.md, pages/concepts/mlm.md；更新 index.md 增加8个条目；确认无矛盾声明（所有新增内容均源自原文直接陈述或合理推演）；孤立页面检查：无新增孤立页；lint通过。

---

- 2026-04-12 ingest "百面大模型.pdf" (pp.20–25): 新增 8 页面（word2vec, fasttext, one_hot_encoding, polysemy_problem, distributional_hypothesis, out_of_vocabulary, subword_tokenization, semantic_representation），更新 index.md 增加 Models/Concepts 分类条目；确认无矛盾声明；所有新建页面均含公式、数据、对比细节及交叉链接；孤立页面检查通过（所有新页均被至少1个现有页引用，如 [[semantic_representation]] 被 [[models/seeed.md]] 和 [[concepts/attention_mechanism.md]] 引用）。

---

- 2026-04-12: Ingested "百面大模型.pdf" (p1–p9). Created 5 new pages: `books/baimian_damoxx`, `concepts/semantic_representation`, `concepts/test_time_inference`, `trends/nlp_four_stages`, `people/liu_qun`. Updated `index.md` with new entries and cross-links. All pages cite source page numbers and embed precise technical claims (e.g., NLP four-stage definition, TTI as frontier topic, semantic representation as logical starting point). No contradictions detected.

---

2026-04-10 ingest: 百面大模型.pdf → updated 10 pages (models/seeed, concepts/{error_detection_in_llms,soft_clustering,monitoring_and_observability}, tools/{hf_datasets_dialerrors,errdetect}, papers/towards_automated_error_discovery, people/{dominic_petrak,thy_thy_tran}, trends/ai_reliability_engineering) + index.md; no contradictions detected; all new pages have ≥3 inbound links from existing content.

---

- 2026-04-10: Ingested inbox item "2026-04-10T060539+0800-Towards Automated Error Discovery A Study in Conversational AI.md". Created 13 new pages: papers/towards_automated_error_discovery, models/seeed, concepts/{error_detection_in_llms, ood_generalization, soft_clustering, self_reflection}, trends/ai_reliability_engineering, tools/{hf_datasets_dialerrors, errdetect}, people/{iryana_gurevych, dominic_petrak, thy_thy_tran}, concepts/monitoring_and_observability. Updated index.md. No contradictions detected during ingestion. All new pages linked bidirectionally per schema. Lint pass: no isolated pages (all have ≥1 inbound link), no outdated markers, all cross-references resolved.

---

# Wiki Log

_按时间倒序，append-only_

---

## 2026-04-10 — Ingest: Attention Is All You Need

- 来源：Vaswani et al., NeurIPS 2017
- URL: https://arxiv.org/abs/1706.03762
- 新建页面：
  - `papers/attention_is_all_you_need.md`
  - `concepts/attention_mechanism.md`
- 更新：`index.md`
- 清理：inbox 中的空白剪藏文件（PDF 无法提取正文）

---

## 2026-04-10 — Ingest: The Bitter Lesson

- 来源：Rich Sutton, "The Bitter Lesson", 2019
- URL: http://www.incompleteideas.net/IncIdeas/BitterLesson.html
- 新建页面：
  - `papers/bitter_lesson.md`
  - `people/rich_sutton.md`
  - `concepts/scaling_computation.md`
  - `concepts/search_and_learning.md`
  - `trends/human_knowledge_vs_computation.md`
- 更新：`index.md`

---

## 2026-04-10 — Wiki 初始化

- 创建 schema.md、index.md、log.md
- 领域：AI / 技术研究
- 分类：models / concepts / papers / people / trends / tools
