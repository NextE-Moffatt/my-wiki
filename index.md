# Wiki Index

_最后更新：2026-04-14_

## Books
- [baimian_damoxx](pages/books/baimian_damoxx.md) — 《百面大模型》，国内首部面试题驱动的大模型全栈技术指南（2025）

## Models
- [seeed](pages/models/seeed.md) — Soft Clustering Extended Encoder-Based Error Detection, EMNLP 2025
- [bert](pages/models/bert.md) — Bidirectional Encoder Representations from Transformers, NAACL 2019
- [gpt](pages/models/gpt.md) — Generative Pre-trained Transformer series, OpenAI 2018–2024
- [word2vec](pages/models/word2vec.md) — Shallow neural network for static dense word embeddings, Mikolov et al. 2013
- [fasttext](pages/models/fasttext.md) — Character n-gram enhanced word embeddings for OOV handling, Bojanowski et al. 2017
- [sbert](pages/models/sbert.md) — Sentence-BERT:孪生BERT微调框架，解决各向异性，STS-B 85.4（Reimers & Gurevych 2019）
- [simcse](pages/models/simcse.md) — Unsupervised contrastive sentence embedding via Dropout-as-augmentation, EMNLP 2021

## Concepts
- [scaling_computation](pages/concepts/scaling_computation.md) — 算力扩展与摩尔定律，AI 核心驱动力
- [search_and_learning](pages/concepts/search_and_learning.md) — 唯二能随算力无限扩展的 AI 技术类别
- [attention_mechanism](pages/concepts/attention_mechanism.md) — 注意力机制原理、Multi-Head Attention、Self/Cross-Attention
- [error_detection_in_llms](pages/concepts/error_detection_in_llms.md) — LLM输出中自动识别有害/错误行为的技术方向
- [ood_generalization](pages/concepts/ood_generalization.md) — 对未见过错误类型与场景的泛化能力
- [soft_clustering](pages/concepts/soft_clustering.md) — 允许样本概率隶属多簇的无监督聚类方法
- [self_reflection](pages/concepts/self_reflection.md) — LLM生成对其自身输出的批判性分析
- [monitoring_and_observability](pages/concepts/monitoring_and_observability.md) — LLM系统可观测性三支柱（metrics/logs/traces）
- [subword_tokenization](pages/concepts/subword_tokenization.md) — 子词分词原理、WordPiece/BPE/Unigram对比、贪心匹配算法
- [word_level_tokenization](pages/concepts/word_level_tokenization.md) — 空格分词实现、OOV脆弱性、与子词方案量化对比
- [position_encoding](pages/concepts/position_encoding.md) — 正弦编码、RoPE、NTK-aware scaling等位置建模技术
- [causal_lm](pages/concepts/causal_lm.md) — 因果语言建模目标函数与实现细节
- [mlm](pages/concepts/mlm.md) — 掩码语言建模原理与性能瓶颈分析
- [one_hot_encoding](pages/concepts/one_hot_encoding.md) — Sparse token representation with zero semantic similarity between distinct tokens
- [distributional_hypothesis](pages/concepts/distributional_hypothesis.md) — “You shall know a word by the company it keeps”: theoretical foundation of word embeddings
- [polysemy_problem](pages/concepts/polysemy_problem.md) — The fundamental challenge of word sense disambiguation in static embeddings
- [contextual_embedding](pages/concepts/contextual_embedding.md) — Dynamic token representations conditioned on full sentence context
- [semantic_representation](pages/concepts/semantic_representation.md) — Mapping language symbols to computable vector spaces with semantic fidelity
- [out_of_vocabulary](pages/concepts/out_of_vocabulary.md) — Out-of-vocabulary (OOV) problem and mitigation strategies across embedding paradigms
- [tokenization](pages/concepts/tokenization.md) — Text-to-symbol mapping as the first semantic gatekeeper in NLP systems
- [character_ngram](pages/concepts/character_ngram.md) — Character n-gram definition, boundary markers, role in FastText and modern fallbacks
- [bpe](pages/concepts/bpe.md) — Byte Pair Encoding: frequency-driven greedy subword merging algorithm
- [wordpiece](pages/concepts/wordpiece.md) — WordPiece: likelihood-driven subword segmentation via EM algorithm
- [word_mover_distance](pages/concepts/word_mover_distance.md) — Word Mover Distance: EMD-based sentence similarity metric, $ O(p^3 \log p) $
- [sentence_embedding](pages/concepts/sentence_embedding.md) — Sentence embedding evaluation via alignment & uniformity metrics
- [alignment_and_uniformity](pages/concepts/alignment_and_uniformity.md) — Formal definitions and optimization of alignment/uniformity for sentence vectors
- [contrastive_learning](pages/concepts/contrastive_learning.md) — Contrastive learning framework: alignment-uniformity tradeoff, InfoNCE loss, positive/negative construction
- [dropout_as_augmentation](pages/concepts/dropout_as_augmentation.md) — Using inherent Dropout stochasticity as free semantic-preserving data augmentation
- [sparse_vs_dense_embeddings](pages/concepts/sparse_vs_dense_embeddings.md) — Fundamental comparison of sparse (one-hot) vs dense (continuous) semantic representations
- [embedding_lookup](pages/concepts/embedding_lookup.md) — Efficient token-to-vector mapping via table lookup, bypassing one-hot construction
- [softmax](pages/concepts/softmax.md) — Softmax function in language modeling; computational bottleneck and normalization properties
- [hierarchical_softmax](pages/concepts/hierarchical_softmax.md) — Hierarchical softmax: Huffman tree-based efficient multi-class classification for large vocabularies
- [negative_sampling](pages/concepts/negative_sampling.md) — Negative sampling: binary classification approximation for softmax in word2vec training
- [stemming](pages/concepts/stemming.md) — Rule-based morphological reduction to stem, used in OOV fallback pipelines
- [edit_distance](pages/concepts/edit_distance.md) — Levenshtein distance as edit operation count; core metric for spelling correction
- [spelling_correction](pages/concepts/spelling_correction.md) — Noisy-channel inspired correction using edit distance + word frequency prior
- [whitespace_tokenization](pages/concepts/whitespace_tokenization.md) — 空格分词实现、OOV脆弱性、与子词方案量化对比
- [wordpiece_algorithm](pages/concepts/wordpiece_algorithm.md) — WordPiece概率驱动合并算法与贪心最长匹配分词
- [edit_operations_for_spelling_correction](pages/concepts/edit_operations_for_spelling_correction.md) — 拼写纠错的4类原子编辑操作及`edits1/edits2`实现
- [subword_composition_for_oov](pages/concepts/subword_composition_for_oov.md) — 子词组合式OOV处理：分解与向量聚合机制
- [lemma_dict_in_embedding_loading](pages/concepts/lemma_dict_in_embedding_loading.md) — 词形还原词典在嵌入加载fallback链中的定位与作用
- [greedy_longest_match](pages/concepts/greedy_longest_match.md) — 贪心最长匹配算法：WordPiece核心解码机制，带边界标记与字符回退
- [bpe_algorithm](pages/concepts/bpe_algorithm.md) — BPE算法：频率驱动的贪心合并流程、确定性分词、`</w>`标记作用
- [character_level_tokenization](pages/concepts/character_level_tokenization.md) — 字符级分词：零先验、语言无关、工业fallback层、量化对比数据
- [sentence_embedding_from_word_vectors](pages/concepts/sentence_embedding_from_word_vectors.md) — 基于词向量的句子嵌入：均值池化公式、工业延迟/QPS数据、SIF改进
- [segment_embedding](pages/concepts/segment_embedding.md) — BERT中用于区分句子段落的二元可学习嵌入，与token/pos嵌入相加
- [position_encoding_decoupling](pages/concepts/position_encoding_decoupling.md) — 词元与位置嵌入在注意力空间中无强相关性，需解耦投影或操作

## Papers
- [bitter_lesson](pages/papers/bitter_lesson.md) — Rich Sutton, 2019；70 年 AI 史的核心教训
- [attention_is_all_you_need](pages/papers/attention_is_all_you_need.md) — Vaswani et al. 2017；Transformer 原始论文
- [towards_automated_error_discovery](pages/papers/towards_automated_error_discovery.md) — Petrak et al., EMNLP 2025；对话AI错误发现新范式
- [rethinking_positional_encoding](pages/papers/rethinking_positional_encoding.md) — Ke et al., ICLR 2023；位置编码解耦的实证研究

## People
- [rich_sutton](pages/people/rich_sutton.md) — 强化学习奠基人，Bitter Lesson 作者
- [iryana_gurevych](pages/people/iryana_gurevych.md) — UKP Lab主任，可信NLP权威，AED论文通讯作者
- [dominic_petrak](pages/people/dominic_petrak.md) — SEEED架构师，AED论文第一作者
- [thy_thy_tran](pages/people/thy_thy_tran.md) — 跨文化错误建模专家，AED论文共同作者

## Trends
- [human_knowledge_vs_computation](pages/trends/human_knowledge_vs_computation.md) — AI 史上反复出现的人类知识 vs 通用计算模式
- [ai_reliability_engineering](pages/trends/ai_reliability_engineering.md) — 将SRE实践迁移到AI系统的新兴工程学科
- [nlp_four_stages](pages/trends/nlp_four_stages.md) — NLP四阶段演进模型：词袋→word2vec→BERT→ChatGPT

## Tools
- [hf_datasets_dialerrors](pages/tools/hf_datasets_dialerrors.md) — 对话错误标注数据集（Hugging Face）
- [errdetect](pages/tools/errdetect.md) — 对话AI错误检测Python工具库（PyPI）
- [flashattention](pages/tools/flashattention.md) — 高效注意力计算内核（CUDA）
- [pagedattention](pages/tools/pagedattention.md) — LLM推理内存管理优化（vLLM）