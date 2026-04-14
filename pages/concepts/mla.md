# Multi-head Latent Attention

_最后更新：2026-04-14_

## 概述  
Multi-head Latent Attention（MLA）是 DeepSeek-R1 提出的注意力变体，通过在 Q/K/V 投影后引入低秩（rank=64）线性变换，压缩中间表示维度，从而显著降低 KV 缓存显存占用与计算开销，同时保持建模能力。

## 详细内容  
### 数学定义  
设标准 MHA 输入为 $X \in \mathbb{R}^{L \times d}$，MLA 操作如下：  
1. 投影：$Q = XW_q,\ K = XW_k,\ V = XW_v$，其中 $W_q,W_k,W_v \in \mathbb{R}^{d \times d}$  
2. **低秩压缩**：$Q' = Q W_q^{\text{low}},\ K' = K W_k^{\text{low}}$，其中 $W_q^{\text{low}}, W_k^{\text{low}} \in \mathbb{R}^{d \times r},\ r=64$  
3. 注意力计算：$\text{Attn} = \text{Softmax}\left( \frac{Q' K'^\top}{\sqrt{r}} \right) (V W_v^{\text{low}})$，$W_v^{\text{low}} \in \mathbb{R}^{d \times r}$  
4. 输出投影：$O = \text{Attn} W_o$，$W_o \in \mathbb{R}^{r \times d}$  

### 关键收益  
- **KV 缓存节省**：标准 MHA 的 KV 缓存为 $2 \times L \times d$，MLA 降为 $2 \times L \times r$ → 当 $d=5120,\ r=64$ 时，显存减少 **98.75%**（即 1/64）  
- **计算量**：QK⊤ 计算从 $O(L^2 d)$ 降至 $O(L^2 r)$，加速比理论达 $d/r = 80\times$（实际受访存限制，实测 3.1×）  
- **无损性验证**：在 LLaMA-2-7B 上替换 MHA 为 MLA（$r=128$），在 MMLU 上精度仅降 0.4%，证实低秩空间足以承载注意力语义  

### 与 RoPE/ALiBi 兼容性  
MLA 可无缝集成 RoPE（旋转位置编码作用于 $Q',K'$）或 ALiBi（线性偏置加在 $Q'K'^\top$ 后），因二者均作用于压缩后的 latent space。

## 相关页面  
[[models/deepseek_r1]] [[concepts/attention_mechanism]] [[concepts/rope]] [[concepts/alibi]] [[concepts/kv_cache_optimization]]

## 来源  
《百面大模型》，第 13.1.2 节 “MLA”，p. 343