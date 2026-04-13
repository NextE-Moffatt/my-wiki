# 多查询注意力（MQA）与分组查询注意力（GQA）

_最后更新：2026-04-13_

## 概述  
多查询注意力（MQA）与分组查询注意力（GQA）是为缓解 Transformer 解码延迟而提出的 KV 共享机制：MQA 令所有 query heads 共享单组 key/value 投影，GQA 将 query heads 分组并共享组内 KV，二者在保持接近 MHA 表达力的同时，显著降低 KV 缓存显存与 attention 计算开销。

## 详细内容  

### 1. 架构对比（《百面大模型》P175, P179）  
| 特性                | MHA（Multi-Head Attention）      | MQA（Multi-Query Attention）       | GQA（Grouped-Query Attention）     |
|---------------------|-----------------------------------|--------------------------------------|---------------------------------------|
| Query heads ($h_q$) | $h_q = 32$（Llama-2-70B）         | $h_q = 32$                           | $h_q = 32$                            |
| Key/Value heads ($h_{kv}$) | $h_{kv} = h_q = 32$             | $h_{kv} = 1$                         | $h_{kv} = 8$（即每组 4 个 Q 共享 1 组 KV） |
| KV 缓存显存         | $2 \times h_q \times d_k \times N$ | $2 \times 1 \times d_k \times N$    | $2 \times h_{kv} \times d_k \times N$ |
| 相对显存节省（vs MHA） | —                                 | **~32×**（Llama-2-70B）             | **~4×**（Llama-3-8B）                |

### 2. 性能权衡（P178–179）  
- **MQA 缺陷**：  
  - 表达力坍缩：所有 query 依赖同一语义通道，损害长程依赖建模（如 Llama-2-70B 使用 MQA 后，HumanEval 代码生成得分下降 8.2%）；  
  - 解码延迟改善有限：因 softmax 计算仍需广播，实际延迟仅降 15–20%。  
- **GQA 优势**：  
  - **帕累托最优**：在 Llama-3-8B 中，GQA（$h_{kv}=8$）使 KV 缓存显存降为 MHA 的 25%，同时 HumanEval 得分仅比 MHA 低 0.7%；  
  - **硬件友好**：分组结构天然匹配 Tensor Core 的 warp-level 并行。  

### 3. 工程实践  
- **部署建议**：  
  - 推理优先场景（如 API 服务）→ 选 MQA（极致低显存）；  
  - 推理+微调兼顾 → 选 GQA（推荐 $h_{kv} = h_q / 4$）；  
- **框架支持**：  
  - vLLM、Hugging Face Transformers（>=4.40）原生支持 `attn_implementation="flash_attention_2"` + `use_cache=True` 自动启用 GQA；  
  - DeepSpeed-Inference 通过 `mpu.get_cuda_rng_tracker().add_ndim_seeds()` 启用 MQA kernel。  

## 相关页面  
[[attention_mechanism]]  
[[pagedattention]]  
[[llama]]  
[[deepseek_r1]]  
[[kv_cache]]  

## 来源  
《百面大模型》，第 6 章 6.8 节 “多头注意力机制及其优化”，P175–179；第 12 页目录：“6.8.3 多查询注意力和分组查询注意力的工作原理”；第 18 页问答：“如何用代码实现多查询注意力和分组查询注意力？”