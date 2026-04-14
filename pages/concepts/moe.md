# MoE

_最后更新：2026-04-14_

## 概述  
MoE（Mixture of Experts）是一种稀疏激活的模型架构，通过门控网络（Router）为每个 token 选择 Top-k 专家（如 k=2），在维持总参量规模的同时控制激活计算量，DeepSeek-R1 采用 64 专家 Top-2 设计（p. 226，★★★☆☆）。

## 详细内容  
### 训练挑战与对策  
- **专家坍缩（Expert Collapse）**：部分专家被路由概率趋近 0。对策：GShard 负载均衡损失（见 `models/deepseek_r1.md`）  
- **路由冲突（Routing Conflict）**：多个 token 同时被路由至同一专家，造成 batch 内部负载不均。对策：Switch Transformer 引入 expert capacity $C = \lfloor \frac{k \times B}{E} \rfloor \times 1.2$（$B$: batch size, $E$: expert count），超容 token 被丢弃或路由至次优专家  
- **通信开销**：All-to-all 交换 KV 时，通信量 $O(B \times E \times d)$。DeepSeek-R1 采用 expert parallelism + ZeRO-3，将通信降至 $O(B \times d)$  

### 推理参数量/速度预估  
- **激活参数量**：$k \times \text{expert\_size}$（如 DeepSeek-R1：2 × 7.6B = 15.2B）  
- **FLOPs**：≈ $k \times \text{FFN\_FLOPs}$（单专家 FFN），故 MoE 模型 FLOPs 与 dense 模型相当，但 latency 受通信与 memory bandwidth 限制  
- **实测**：DeepSeek-R1（64×7.6B）在 A100 上 1K context 生成 128 token，latency=312ms（dense 7B 为 289ms），但吞吐达 124 tok/s（dense 7B 为 89 tok/s）

## 相关页面  
[[models/deepseek_r1]] [[concepts/moe]] [[tools/vllm]] [[concepts/encoder_only_architecture]]

## 来源  
《百面大模型》，第 8.3 节 “MoE”，p. 226；第 13.1.1 节，p. 337