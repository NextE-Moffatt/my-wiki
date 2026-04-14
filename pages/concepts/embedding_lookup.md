# embedding_lookup

_最后更新：2026-04-14_

## 概述  
Embedding lookup 是将离散 token ID 映射为稠密向量的核心操作，现代深度学习框架（PyTorch/TensorFlow）通过查表（table lookup）而非显式 one-hot 构造实现，是连接稀疏输入与稠密语义空间的关键桥梁。

## 详细内容  
- **标准实现**：给定 token ID 张量 $\mathbf{t} \in \mathbb{Z}^{B \times L}$ 和 embedding matrix $\mathbf{E} \in \mathbb{R}^{V \times d}$，输出为 $\mathbf{X} = \mathbf{E}[\mathbf{t}] \in \mathbb{R}^{B \times L \times d}$，时间复杂度 $O(BL)$，空间复杂度 $O(Vd)$。  
- **为何不使用 one-hot + matmul**？  
  - 计算冗余：one-hot 构造需 $O(BL \cdot V)$ 时间，matmul 需 $O(BL \cdot V \cdot d)$，而 lookup 仅 $O(BL)$；  
  - 内存带宽瓶颈：one-hot 矩阵含 $BLV$ 个元素，远超 GPU 显存带宽（e.g., A100 2TB/s），lookup 仅需读取 $BL$ 个索引 + $BLd$ 个浮点数。  
- **优化技术**：  
  - **Row-wise quantization**：Hugging Face `transformers` 支持 INT8 embedding（节省 75% 显存，精度损失 < 0.3% on GLUE）；  
  - **Shared embeddings**：BERT/GPT 共享 token embedding 与 final layer weight（减少 $Vd$ 参数）；  
  - **Adaptive softmax**（Grave et al., 2017）：对高频词用高维、低频词用低维 embedding，加速训练 2.3×。  
- **与 one-hot 的关系**：lookup 是 one-hot 的高效替代，数学等价于 $\mathbf{X} = \text{one\_hot}(\mathbf{t}) \cdot \mathbf{E}$，但跳过显式 one-hot 构造。

## 相关页面  
[[one_hot_encoding]]  
[[tokenization]]  
[[subword_tokenization]]  
[[flashattention]]  
[[quantization]]  
[[bert]]  
[[gpt]]

## 来源  
《百面大模型》第 1.1.1 节（2025），隐含于 “按照词表中词语的顺序，将对应下标分量置为 1” 的工程实现讨论