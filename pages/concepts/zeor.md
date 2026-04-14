# ZeRO（Zero Redundancy Optimizer）

_最后更新：2026-04-14_

## 概述  
ZeRO 是微软 DeepSpeed 提出的模型并行优化技术，通过分片（sharding）优化器状态、梯度、模型参数，消除数据并行中的内存冗余，在不牺牲通信效率前提下支持万卡级训练。

## 详细内容  
ZeRO 分三级（据第 3.6.5 节）：
- **ZeRO-1**：分片优化器状态（momentum、variance），显存节省 ≈ 33%（optimizer state 占比最高）；
- **ZeRO-2**：分片梯度 + ZeRO-1，显存节省 ≈ 66%（梯度与 optimizer state 共占 ~80%）；
- **ZeRO-3**：分片模型参数 + ZeRO-2，显存节省 ≈ 85–95%，支持 1T+ 参数模型（如 Megatron-Turing NLG 530B）。

通信开销公式（batch size $B$，模型参数量 $P$，数据并行度 $D$）：
- ZeRO-1：$ \text{comm} = \frac{2P}{D} $（all-reduce optimizer states）
- ZeRO-2：$ \text{comm} = \frac{2P}{D} + \frac{2P}{D} = \frac{4P}{D} $（states + gradients）
- ZeRO-3：$ \text{comm} = \frac{2P}{D} $（仅 broadcast parameters on demand，无 all-reduce）

关键实践（第 3.6.5 节）：
- ZeRO-3 需配合 CPU offload（将部分状态卸载至 CPU RAM）以缓解 GPU 显存压力；
- 通信与计算重叠：使用 NCCL async all-reduce + CUDA graph，重叠率可达 92%；
- 性能拐点：当 $D > 64$ 时，ZeRO-3 的通信开销开始超过数据并行，建议切换至混合并行（ZeRO-3 + Tensor Parallelism）。

## 相关页面  
[[deepspeed]] [[tensor_parallelism]] [[data_parallelism]] [[megatron]] [[communication_efficiency]]

## 来源  
《百面大模型》，第 3 章 3.6.5 节（pp. 85–87），2025 年出版