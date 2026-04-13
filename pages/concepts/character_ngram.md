# 字符n-gram（Character n-gram）

_最后更新：2026-04-13_

## 概述  
字符n-gram是将单词按固定长度 `n` 的连续字符窗口滑动切分所得的所有子串集合，是解决OOV问题的底层原子单元，被FastText等模型直接用于词向量构造。

## 详细内容  

### 1. 定义与生成规则  
- 对单词 `w`，添加边界符号 `<` 和 `>`，生成所有长度为 `n` 的子串；  
- 例（`n=3`, `w=applet`）：`<ap`, `app`, `ppl`, `ple`, `let`, `et>`；  
- **边界符号必要性**：区分词首/词尾（`<ap` ≠ `tap`），避免歧义；  
- **n的选择**：`n=3`（trigram）最常用——平衡覆盖率（`n=2` 过泛）与特异性（`n=5` 过稀疏）。

### 2. 数学性质与优势  
- **完备性**：26个小写字母 + 26个大写字母 + `<`, `>` 共54符号，可生成任意英文单词的n-gram，理论OOV率为0；  
- **共享性**：`process` 与 `processor` 共享 `pro`, `roc`, `ocess` 等n-gram，向量空间自然诱导语义相似性；  
- **鲁棒性**：对拼写错误（`recieve` → `rec`, `eci`, `civ`, `ive>`）仍能复用大量正确n-gram，保持部分语义。

### 3. 在现代系统中的角色  
- **FastText**：直接作为嵌入基元（见 `fasttext.md`）；  
- **Transformer tokenizer fallback**：Hugging Face `tokenizers` 库中，当子词切分失败时启用 `byte_fallback=True`，将UTF-8字节序列转为字节n-gram；  
- **多语言适配**：对无空格语言（中文、日文），字符n-gram是唯一可行的无监督切分起点（如 `北京大学` → `北京`, `京大`, `大学`）。

## 相关页面  
[[concepts/subword_tokenization]]  
[[models/fasttext]]  
[[concepts/out_of_vocabulary]]  
[[concepts/tokenization]]  
[[tools/hf_datasets_dialerrors]]（错误标注中`spelling_error`类型依赖n-gram异常检测）

## 来源  
《百面大模型》第1章第1.3节，p.29：“FastText 是这种思路的代表性方法...例如，对于一个溢出词表词applet，如果设置n-gram的n为3 (3-gram)，那么溢出词表词applet 就会被分解为app、ple、let 这3个n-gram 集合。”