# MQA 与 GQA（Multi-Query / Grouped-Query Attention）

_最后更新：2026-04-14_

## 概述  
MQA（Multi-Query Attention）与 GQA（Grouped-Query Attention）是为缓解 Transformer 解码器 KV cache 显存瓶颈而提出的注意力变体：MQA 共享全部 query 头的 key/value 投影，GQA 则将 query 头分组共享 KV 投影，在显存效率与建模能力间取得平衡。

## 详细内容  
设模型有 $h_q$ 个 query 头、$h_k = h_v$ 个 key/value 头：
- **MQA**：$h_k = h_v = 1$，所有 $h_q$ 个 query 头复用同一组 KV 投影；显存节省率 = $1 - \frac{2}{2h_q} = 1 - \frac{1}{h_q}$（如 LLaMA-2-7B 的 $h_q=32$，节省 96.9% KV cache）；
- **GQA**：$h_k = h_v = g$（$g < h_q$），每 $h_q/g$ 个 query 头共享一组 KV 投影；典型配置 $g=8$（Qwen1.5-7B）、$g=4$（DeepSeek-V2）；显存节省率 = $1 - \frac{2g}{2h_q} = 1 - \frac{g}{h_q}$。

据第 6.8 节性能分析：
- **解码延迟**：MQA 推理吞吐提升 1.8×（vs MHA），但因信息瓶颈导致 3–5% 任务性能下降（MMLU、GSM8K）；GQA 在吞吐（+1.5×）与精度（<0.5% 下降）间更优；
- **硬件适配**：MQA/GQA 的 KV cache 可压缩为连续张量，与 PagedAttention 内存池天然兼容（见 [[pagedattention]]）；
- **实现约束**：需修改 attention kernel（如 FlashAttention-2 支持 `is_causal=True` + `window_size=None` + `alibi_slopes=None` 下的 MQA/GQA 模式）。

> ⚠️ 矛盾：本书称“GQA 精度损失 <0.5%”，但 DeepSeek-V2 技术报告（2024）指出其 GQA（$g=8$）在 HumanEval 上比 MHA 低 2.1 分。差异可能源于评估集或 baseline 设置，需标注。

## 相关页面  
[[multi_query_attention]] [[grouped_query_attention]] [[pagedattention]] [[flashattention]] [[deepseek_r1]] [[llama]] [[qwen]]

## 来源  
《百面大模型》，第 6 章 6.8 节（pp. 175–180），2025 年出版