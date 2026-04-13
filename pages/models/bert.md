# BERT

_最后更新：2026-04-13_

## 概述  
BERT（Bidirectional Encoder Representations from Transformers）是首个成功实现**全上下文双向语义建模**的预训练语言模型，其核心创新在于输入层的三重嵌入叠加机制（词元+位置+分段嵌入）及MLM预训练目标；但后续研究发现该叠加设计存在语义耦合缺陷，需在注意力计算中解耦位置信息以提升性能。

## 详细内容  

### 输入嵌入结构与特征交叉机制  
BERT 的输入由三个独立嵌入向量相加构成：  
- **词元嵌入（token embedding）**：基于子词分词（WordPiece），中文使用**中文字符级粒度**，英文使用**字节对编码（BPE）**；相比词级分词更粗粒度，显著压缩词表稀疏性（长尾词从稀疏→稠密），但牺牲部分词义个性化表达能力。  
- **位置嵌入（position embedding）**：正弦函数生成的绝对位置编码，维度与词元嵌入一致（768/1024），用于引入序列顺序信息。  
- **分段嵌入（segment embedding）**：二值化标识句子A/B（如[CLS]句对任务），支持NSP任务。  

三者**逐元素相加**（而非拼接或池化），本质是神经网络中一种**低阶特征交叉操作**，旨在构造“带位置感知的上下文化词元表示”。该设计使模型能为同一字符（如“苹果”中的“果”）在不同位置赋予差异化向量，缓解Transformer因无显式位置建模导致的上下文感知退化问题。

> ⚠️ 矛盾：原文称“相加是特征交叉”，但《Rethinking Positional Encoding in Language Pre-training》指出：词元与位置嵌入在Q/K/V映射中**共享权重矩阵**，且可视化显示二者相关性矩阵（词元→位置、位置→词元）呈均匀分布（图1-8），证明二者**语义关联极弱**；强行相加引入虚假交互，反降低建模效率。

### 位置嵌入解耦的实证改进  
该论文提出将位置嵌入从输入层剥离，改为在自注意力计算中**独立注入**：  
原始注意力权重公式展开后含四项：  
$$
a_{ij} = \frac{((w_i + p_i)W^Q)^T ((w_j + p_j)W^K)}{\sqrt{d_k}} = \frac{(w_i W^Q)^T (w_j W^K)}{\sqrt{d_k}} + \frac{(w_i W^Q)^T (p_j W^K)}{\sqrt{d_k}} + \frac{(p_i W^Q)^T (w_j W^K)}{\sqrt{d_k}} + \frac{(p_i W^Q)^T (p_j W^K)}{\sqrt{d_k}}
$$  
其中中间两项（$w_i\leftrightarrow p_j$ 和 $p_i\leftrightarrow w_j$）被证实无统计显著性（图1-8中第二、三矩阵均匀），故可安全移除，得到解耦形式：  
$$
a_{ij}^{\text{decoupled}} = \frac{(w_i W^Q)^T (w_j W^K)}{\sqrt{d_k}} + \frac{(p_i W_p^Q)^T (p_j W_p^K)}{\sqrt{d_k}}
$$  
实验表明：此解耦方案使**预训练损失收敛更快**，且下游任务（如SQuAD、MNLI）**平均提升1.2–2.4个点**。

### 架构定位与能力边界  
- 属于**纯编码器（encoder-only）架构**：仅支持NLU任务（如分类、匹配、抽取），**天然缺乏生成能力**；需通过前缀语言模型（prefix-LM）变体（如BART的encoder部分）或二次微调适配生成场景。  
- 在NLP四阶段演进中代表**第三阶段（深层表征）**，上承word2vec（浅层表征），下启ChatGPT（大模型表征）。  
- 与GPT系列对比：BERT依赖**MLM掩码重建**，GPT依赖**因果LM（causal LM）**；前者适合理解，后者适合生成。

## 相关页面  
[[models/gpt]] [[models/word2vec]] [[concepts/mlm]] [[concepts/causal_lm]] [[concepts/position_encoding]] [[concepts/encoder_only_architecture]] [[papers/rethinking_positional_encoding]] [[trends/nlp_four_stages]]

## 来源  
《百面大模型》，第44–45页；第47–48页（架构分类）；第49页（数据阶段说明）