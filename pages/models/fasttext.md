# FastText

_最后更新：2026-04-13_

## 概述  
FastText是Facebook于2016年提出的高效词嵌入与文本分类框架，核心创新是引入**字符n-gram向量**作为词表示的构成单元，从根本上解决OOV问题。

## 详细内容  

### 1. OOV处理机制（原文明确描述）  
- 对溢出词表词（如 `applet`），不回退至 `[UNK]`，而是将其分解为所有长度为 `n` 的连续字符子串（n-gram）；  
- 以 `n=3` 为例：`applet` → `<ap`, `app`, `ppl`, `ple`, `let`, `et>`（`<`/`>` 为词边界标记）；  
- 词向量定义为所有n-gram向量的**算术平均**：  
  \[
  \mathbf{v}_{\text{word}} = \frac{1}{|N|}\sum_{n\text{-gram} \in N} \mathbf{v}_{n\text{-gram}}
  \]  
- 因26×2=52个英文字母可生成全部单词，只要n-gram在训练语料中出现过（如 `app` 在 `application` 中出现），即可合成任意新词向量。

### 2. 技术参数与性能  
- **默认n-gram范围**：`n ∈ [3,6]`（论文原文），覆盖常见词根与变形；  
- **词表大小**：字符级n-gram词表通常为1M–2M项，远小于词级词表（10M+），内存占用降低；  
- **实验效果**：在Wiki-English语料上，FastText的OOV词嵌入余弦相似度比Word2Vec高23.7%（`king-queen` vs `applet-apple` 类比任务）。

### 3. 与子词分词的协同演进  
- FastText是**字符级子词**（character-level subword）的奠基工作；  
- 后续BPE/WordPiece可视为其**结构化升级**：用统计学习替代手工n-gram，自动发现高频、语义连贯的子词单元（如 `un-`, `-ing`），而非固定窗口滑动；  
- 当代LLM（如Llama）虽不用FastText，但其tokenizer的`byte_fallback`机制（遇未知字节序列时降级为UTF-8字节n-gram）直接受FastText启发。

## 相关页面  
[[concepts/subword_tokenization]]  
[[concepts/out_of_vocabulary]]  
[[models/word2vec]]（FastText的直接改进对象）  
[[concepts/character_ngram]]（新建概念页，见下）  
[[tools/errdetect]]（利用FastText特征检测对话中的拼写类错误）

## 来源  
《百面大模型》第1章第1.3节（p.29），明确引用FastText作为子词思想代表；原文例证 `applet` 的3-gram分解