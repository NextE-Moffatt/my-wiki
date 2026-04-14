# 位置编码

_最后更新：2026-04-14_

## 概述  
位置编码（Position Encoding）是向 Transformer 类模型注入序列顺序信息的核心机制，用于弥补自注意力机制本身不具备位置感知能力的缺陷；其设计直接影响模型对语序敏感任务（如关系分类、依存分析）的建模能力与外推性能。

## 详细内容  

### 一、必要性：语序敏感性实证  
- 在**关系分类任务**中，头实体与尾实体的**相对顺序决定语义**（如“奥巴马→美国” vs “美国→奥巴马”），错误顺序将导致关系类别误判。  
- 实践方案：引入 4 个特殊符号（`[HEAD_S]`, `[HEAD_E]`, `[TAIL_S]`, `[TAIL_E]`），**共享其位置编码与对应实体边界字符的位置编码**，使特殊符号向量隐式携带实体位置信息，再拼接输入分类器。  
- 表格示例（文本 `"亲密的母亲在美国"`，头实体 `"母亲"` 起止位置 3–4，尾实体 `"美国"` 起止位置 9–10）：  
  | 文本 | `[HEAD_S]` | `[HEAD_E]` | `[TAIL_S]` | `[TAIL_E]` | 亲 | 密 | 的 | 母 | 亲 | 在 | 美 | 国 |  
  |------|------------|------------|------------|------------|----|----|----|----|----|----|----|----|  
  | 位置 | 0          | 2          | 7          | 8          | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  |  

### 二、绝对位置编码（Absolute PE）  
#### 1. 训练式（BERT 风格）  
- 形式：可学习参数矩阵 `pos_emb ∈ ℝ^(seq_len × hidden_size)`，随模型训练更新。  
- **关键限制：无法外推**（out-of-sequence extrapolation）——当输入长度 > `seq_len` 时，无定义位置向量，导致推理失败。  
- 典型值：BERT-base 使用 `seq_len = 512`, `hidden_size = 768`。  

#### 2. Sinusoidal（Transformer 原始方案）  
- 公式：  
  $$
  \begin{cases}
  p_{k,2i} = \sin\left(k / 10000^{2i/d}\right) \\
  p_{k,2i+1} = \cos\left(k / 10000^{2i/d}\right)
  \end{cases}
  $$  
  其中 $k$ 为位置索引，$i$ 为维度索引（$0 \leq i < d/2$），$d = \text{hidden\_size}$。  
- **两大理论优势**：  
  (1) **线性可组合性**：任意偏移 $k_{\text{offset}}$，有  
  $$
  \boldsymbol{p}(k + k_{\text{offset}}) = \mathbf{A}_{k_{\text{offset}}} \boldsymbol{p}(k) + \mathbf{B}_{k_{\text{offset}}} \boldsymbol{p}(k_{\text{offset}})
  $$  
  （由 $\cos(a+b)=\cos a \cos b - \sin a \sin b$ 等三角恒等式保证），使模型可线性学习相对位置。  
  (2) **值域稳定性**：所有分量 ∈ $[-1, 1]$，与 $k$ 无关，保障梯度训练稳定性。  
- **不参与训练**：`p_k` 是固定函数生成，无梯度更新。  

### 三、相对位置编码（Relative PE）  
- 核心思想：在注意力得分计算中**显式建模位置差 $i-j$**，而非仅依赖绝对位置。  
- 基础公式（Shaw et al., 2018）：  
  $$
  o_i = \sum_j a_{i,j} \left( x_j W_v + R_{i,j}^v \right), \quad 
  a_{i,j} = \text{softmax}\left( \boldsymbol{q}_i \boldsymbol{k}_j^T + \boldsymbol{q}_i R_{i,j}^K \right)
  $$  
  其中 $R_{i,j}^v, R_{i,j}^K$ 是依赖 $i-j$ 的可学习或函数化矩阵（如 RoPE 用旋转矩阵，ALiBi 用线性偏差）。  
- **演进脉络**：XLNet → T5 → DeBERTa → RoPE → ALiBi，均围绕对 $\boldsymbol{q}_i \boldsymbol{k}_j^T$ 的展开式进行结构化增强，目标包括：  
  - 提升长程依赖建模（RoPE 的旋转不变性）  
  - 增强外推能力（ALiBi 的线性衰减偏差）  
  - 融合绝对+相对信息（DeBERTa 的解耦式双编码）  

### 四、嵌入相加的深层机理（BERT 场景）  
- BERT 输入 = `token_emb + pos_emb + seg_emb`（三者同维，直接相加）。  
- **非池化，而是特征交叉**：因三者向量空间语义正交（词义 vs 位置 vs 句子段落），加法强制模型学习跨模态交互，提升个性化词元表征。  
- **为何不拼接？**  
  - ✅ 维度守恒：保持 `hidden_size` 不变，避免后续层参数量爆炸；  
  - ✅ 抑制过拟合：拼接允许模型单独放大某类嵌入权重，易导致对位置/分段信号的过度依赖；  
  - ❌ 无信息增益：实验表明拼接未显著提升下游任务性能（见 *Rethinking Positional Encoding*）。  

### 五、批判性发现（Rethinking Positional Encoding）  
- 对 $\alpha_q = \frac{((w_i + p_i)W^Q)((w_j + p_j)W^K)^T}{\sqrt{d}}$ 展开得四项：  
  $$
  \underbrace{\frac{(w_i W^Q)(w_j W^K)^T}{\sqrt{d}}}_{\text{token-token}} + 
  \underbrace{\frac{(w_i W^Q)(p_j W^K)^T}{\sqrt{d}}}_{\text{token-pos}} + 
  \underbrace{\frac{(p_i W^Q)(w_j W^K)^T}{\sqrt{d}}}_{\text{pos-token}} + 
  \underbrace{\frac{(p_i W^Q)(p_j W^K)^T}{\sqrt{d}}}_{\text{pos-pos}}
  $$  
- **可视化证据（图 1-8）**：中间两项（token-pos & pos-token）相关性矩阵呈均匀分布，证明**词元与位置无强语义关联**；且共享 $W^Q/W^K$ 矩阵不合理（二者信息本质不同）。  
- **结论**：应解耦 token 和 position 的投影路径，或移除 token-pos/pos-token 交叉项（如 RoPE 将位置信息注入旋转操作，而非直接相加）。  

## 相关页面  
[[concepts/attention_mechanism]] [[concepts/rope]] [[concepts/alibi]] [[concepts/position_encoding_decoupling]] [[papers/attention_is_all_you_need]] [[papers/rethinking_positional_encoding]] [[models/bert]] [[models/transformer]] [[concepts/subword_tokenization]] [[concepts/segment_embedding]]

## 来源  
《百面大模型》第 1.6–1.8 节；Vaswani et al. (2017) "Attention Is All You Need"；Shaw et al. (2018) "Self-Attention with Relative Position Representations"；Ke et al. (2023) "Rethinking Positional Encoding in Language Pre-training"