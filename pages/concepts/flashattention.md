# FlashAttention

_最后更新：2026-04-14_

## 概述  
FlashAttention 是一种 I/O-aware 的高效注意力计算内核，通过分块（tiling）、重计算（recomputation）与共享内存优化，显著降低 HBM 访问次数，在保持数值精度的同时加速训练与推理。

## 详细内容  
标准注意力计算 $\text{Softmax}(QK^\top/\sqrt{d})V$ 的瓶颈在于：$QK^\top$ 中间矩阵需完整存入 HBM（显存带宽成为瓶颈）。FlashAttention 将 $Q,K,V$ 按块切分（如 $256\times d$），在 SRAM 中完成块内 softmax + dropout + weighted sum，仅写回最终输出 $O$，HBM 访问量从 $O(N^2d)$ 降至 $O(Nd\sqrt{N})$。

据第 12.3 节实测数据（A100-80G）：
- **训练加速**：BERT-large 预训练 step time 降低 17%（vs PyTorch SDPA）；
- **推理吞吐**：LLaMA-2-7B 在 batch=1、seq_len=2048 时，decode latency 降低 23%，P99 延迟从 42ms → 32ms；
- **显存节省**：KV cache 占用减少 15%（因避免中间矩阵存储），与 RoPE 结合时效果叠加（总显存节省达 22%）；
- **支持特性**：原生支持 causal mask、ALiBi bias、RoPE、MQA/GQA（FlashAttention-2）。

FlashAttention-2 进一步优化：将 softmax 归一化拆分为 two-pass（first pass for max, second for sum），消除 warp divergence；FLOPs 降低 2.4×，实际加速比达 3.0×（vs v1）。

## 相关页面  
[[flashattention]] [[pagedattention]] [[rope]] [[alibi]] [[mqa_gqa]] [[attention_mechanism]]

## 来源  
《百面大模型》，第 12 章 12.3 节（pp. 297–305），2025 年出版