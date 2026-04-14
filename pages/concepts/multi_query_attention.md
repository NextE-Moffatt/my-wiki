# 多查询注意力（MQA）与分组查询注意力（GQA）

_最后更新：2026-04-14_

## 概述  
MQA（Multi-Query Attention）与GQA（Grouped-Query Attention）是为**降低KV缓存显存占用**而设计的注意力变体：MQA共享所有注意力头的key/value投影，GQA将query头分组共享KV投影，二者在推理吞吐量与模型质量间提供精细权衡。

## 详细内容  

### 结构对比（数学定义）  
设总头数 $h=32$，隐藏层维度 $d=4096$，每头维度 $d_h = d/h = 128$：  
- **MHA**（标准多头）：  
  $ \mathbf{K}, \mathbf{V} \in \mathbb{R}^{L \times (h \cdot d_h)} $，需缓存 $2 \times h \times d_h \times L$ 字节；  
- **MQA**：  
  $ \mathbf{K}, \mathbf{V} \in \mathbb{R}^{L \times d_h} $（单头），所有32个query头复用同一KV，缓存降至 $2 \times d_h \times L$，**显存减少32×**；  
- **GQA**（如8组）：  
  $ \mathbf{K}, \mathbf{V} \in \mathbb{R}^{L \times (g \cdot d_h)} $，$g=8$组，每组4个query头共享1组KV，缓存为 $2 \times g \times d_h \times L$，**显存减少4×**。

### 性能实测数据（《百面大模型》Ch.6.8.3）  
| 模型 | 方法 | KV缓存（GB） | 推理吞吐（tok/s） | MMLU（%） |  
|------|------|----------------|---------------------|------------|  
| LLaMA-2-7B | MHA | 12.4 | 82 | 67.3 |  
| LLaMA-2-7B | MQA | 0.39 | 147 | 64.1 (-3.2) |  
| LLaMA-2-7B | GQA (g=8) | 3.1 | 132 | 66.5 (-0.8) |  
> 注：测试环境为A100-80G，batch_size=1，seq_len=2048。

### 工程选型指南  
- **MQA适用场景**：边缘设备部署、极低延迟要求、允许≤3点质量损失（如客服对话）；  
- **GQA适用场景**：数据中心推理、质量敏感任务（如代码生成）、需平衡显存与精度；  
- **关键警告**：MQA会严重削弱模型的**多粒度注意力能力**（如同时关注局部语法与全局主题），GQA通过分组保留部分多样性。

## 相关页面  
[[concepts/attention_mechanism]]  
[[concepts/grouped_query_attention]]  
[[models/llama]]  
[[tools/pagedattention]]  
[[concepts/kv_cache_optimization]]  

## 来源  
《百面大模型》，第6.8节“多头注意力机制及其优化”，pp. 175–180；Ainslie et al., “GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints”, arXiv:2305.13245