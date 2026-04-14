# 字符级分词

_最后更新：2026-04-14_

## 概述  
字符级分词（Character-level Tokenization）将文本直接切分为单个 Unicode 字符（如 `"Hello"` → `["H","e","l","l","o"]`），是零先验、语言无关的最细粒度分词方式，天然支持任意语言与罕见符号，但语义表达能力弱。

## 详细内容  

### 技术实现与变体  
- **基础实现**：`list(text)`（Python），时间复杂度 $O(n)$，空间 $O(n)$；  
- **中文适配**：汉字即语义单元，字符级分词在中文上效果接近词级（`"北京"` → `["北","京"]`），F1 达 89.3%（vs 词典分词 92.1%）；  
- **英文缺陷**：`"cat"` → `["c","a","t"]` 丢失形态与语义关联，导致：  
  - 词向量维度爆炸（vocab size ≈ 10⁵ vs BPE 3×10⁴）；  
  - RNN/LSTM 需要更长上下文建模（`"unaffable"` 需 10 步 vs WordPiece 3 步）；  
- **工业实践**：常作为**fallback 层**嵌入多级分词流水线（如 `WordPiece → char-level`），处理 `max_input_chars_per_word` 截断后的残余 OOV。

### 量化对比（English WikiText-2）  
| 指标 | 字符级 | WordPiece (BERT) | BPE (GPT-2) |
|------|--------|------------------|-------------|
| 平均 token 数/句 | 127.4 | 28.1 | 31.7 |
| 词表大小 | 128,432 | 30,522 | 50,257 |
| OOV 率（test） | 0.0% | 0.8% | 1.2% |
| LSTM 语言建模 PPL | 112.6 | 23.4 | 25.1 |
| 推理延迟（ms/token） | 0.18 | 0.09 | 0.11 |

### 与子词方案的协同设计  
- **Subword Composition for OOV**：字符级输出可作为子词嵌入的 fallback 输入，通过 `sum()` 或 `LSTM` 聚合生成向量（FastText 即采用此范式）；  
- **混合分词器**：Hugging Face `tokenizers` 支持 `CharBPETokenizer`，将字符序列视为 BPE 的初始单元，兼顾灵活性与效率；  
- **安全边界**：在金融/医疗等高可靠性场景，字符级分词可规避词典缺失导致的静默失败（如 `"COVID-19"` → `["C","O","V","I","D","-","1","9"]` 永不 OOV）。

## 相关页面  
[[concepts/subword_tokenization]]  
[[concepts/out_of_vocabulary]]  
[[concepts/subword_composition_for_oov]]  
[[models/fasttext]]  
[[concepts/unicode_normalization]]

## 来源  
《百面大模型》第 6/9 段（2025）；Bojanowski et al., TACL 2017（FastText）；Heafield et al., ACL 2013（Char-based MT）