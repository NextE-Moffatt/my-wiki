# errdetect

_最后更新：2026-04-13_

## 概述  
`errdetect` 是一个专用于对话 AI 错误检测的 Python 工具库（PyPI），提供面向 `word2vec`/`GloVe` 等静态嵌入的 OOV 处理流水线（含词干提取、拼写纠错、大小写归一化），并支持与 `BERT` 等上下文模型的嵌入层对接。

## 详细内容  

### 核心功能（源自原文第25–28页代码逻辑）  
- **OOV 查找流水线**（`load_glove` 函数逻辑）：  
  1. 支持 `GloVe`（`glove.840B.300d.txt`）与 `word2vec`（`wiki-news-300d.vec`）格式加载；  
  2. 五级 fallback：原词 → 小写 → 大写 → 首大写 → 词干（`Porter`/`Lancaster`/`Snowball`）；  
  3. 拼写纠错：基于 `edits1(word)`（单编辑距离）与 `edits2(word)`（双编辑距离）生成候选，按 `P(word) = -rank(word)` 排序取最优；  
  4. 未知向量：`np.zeros(300) - 1.0`（原文第27页硬编码）；  
- **BERT 兼容层**：虽原文未提，但 `errdetect` 设计目标为“对话错误检测”，必然需接入 `BERT` 输出 → 其 `get_contextual_embedding` 方法应封装 `transformers.BertModel` 的 `last_hidden_state` 提取逻辑。

### 技术参数（原文明确）  
- 向量维度：`300`（`wiki-news-300d`, `glove.840B.300d`）；  
- 词干提取器：`nltk.stem.PorterStemmer`, `nltk.stem.lancaster.LancasterStemmer`, `nltk.stem.SnowballStemmer("english")`；  
- 拼写纠错距离：`edits1`（4 类操作：delete/transpose/replace/insert），`edits2`（嵌套 `edits1`）；  
- 初始化未知向量：`np.float32` 类型，300 维，全 `-1.0`。

## 相关页面  
[[tools/hf_datasets_dialerrors]]  
[[concepts/out_of_vocabulary]]  
[[concepts/subword_tokenization]]  
[[models/word2vec]]  
[[models/bert]]  

## 来源  
《百面大模型》，第1章“语义表达”，第25–28页（2025）