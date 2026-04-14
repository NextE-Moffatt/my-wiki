# Sentence Embedding from Word Vectors

_最后更新：2026-04-14_

## 概述  
基于静态词向量（如 word2vec、FastText）构建句子向量的两类主流方法：均值池化（unweighted average）与 TF-IDF 加权平均；二者均通过聚合词向量生成固定维句子表征，适用于毫秒级响应场景（如语音智能客服），但存在语序缺失、语义漂移、OOV 敏感等固有局限。

## 详细内容  

### 1. 均值池化（Unweighted Average）  
给定句子 $S = \{w_0, w_1, ..., w_{n-1}\}$，其词向量为 $\{\mathbf{EMB}_0, \mathbf{EMB}_1, ..., \mathbf{EMB}_{n-1}\} \in \mathbb{R}^d$，句子向量定义为：  
$$
\mathbf{S}_{\text{avg}} = \frac{1}{n} \sum_{i=0}^{n-1} \mathbf{EMB}_i
$$  
- ✅ 优势：无需额外训练、计算开销极低（O(n) 时间 + O(d) 空间）、工业级 QPS 可达 >50k/s（实测于 16-core CPU + FP32 向量库）  
- ❌ 缺陷：  
  - 忽略词重要性（如“not”、“very”等修饰词权重未体现）；  
  - 长文本语义漂移显著（>50 token 时 STS-B 相关性下降 ≥28%）；  
  - 对分词质量高度敏感（空格/子词切分误差直接放大至句向量）；  
  - 完全丢失语序与句法结构信息（“猫追狗” ≡ “狗追猫”）。

### 2. TF-IDF 加权平均  
引入词频-逆文档频率权重 $\text{tfidf}_i$（基于大规模语料统计），句子向量为：  
$$
\mathbf{S}_{\text{tfidf}} = \sum_{i=0}^{n-1} \frac{\mathbf{EMB}_i \cdot \text{tfidf}_i}{\sum_j \text{tfidf}_j}
$$  
- ✅ 改进：在短文本（≤15 token）上 STS-B 相关性提升 3.2–5.7 pts（vs. unweighted）；对关键词（如命名实体、动词）赋予更高表征权重。  
- ❌ 局限：  
  - 仍无法建模上下文依赖（“Apple” 在 “Apple Inc.” vs. “apple pie” 中向量相同）；  
  - TF-IDF 统计依赖外部语料分布，跨领域迁移性能骤降（新闻→医疗语料 drop ≥12.4 pts）；  
  - 未解决各向异性（anisotropy）问题：词向量空间呈尖锐锥形分布，导致余弦相似度饱和（cosine > 0.95 占比达 63%）。

### 3. 工业部署约束与实证数据  
- **延迟要求**：语音智能客服端到端响应需 ≤80ms（含 ASR+语义匹配+TTS），其中向量相似度计算（FAISS L2 search）必须 <5ms；  
- **硬件适配**：均值池化可在 ARM Cortex-A76（4GB RAM）嵌入式设备实时运行（<3ms），而 WMD 或 BERT 类模型不可行；  
- **fallback 链**：当 subword_tokenization 失败时，退化至 character_level_tokenization → character_ngram 聚合，此时均值池化仍是唯一可行方案。

## 相关页面  
[[concepts/word2vec]] [[concepts/fasttext]] [[concepts/glove]] [[concepts/word_level_tokenization]] [[concepts/subword_tokenization]] [[concepts/character_level_tokenization]] [[concepts/ood_generalization]] [[concepts/semantic_representation]] [[concepts/sentence_embedding]] [[concepts/alignment_and_uniformity]]

## 来源  
《百面大模型》第 1.5 节（2025），P7；原文明确给出公式、工业场景约束（语音客服毫秒级）、实测性能衰减数据（长文本↓28%）、TF-IDF 短文本增益（3.2–5.7 pts）、各向异性现象（cosine > 0.95 占比 63%）、嵌入式设备延迟（<3ms）。