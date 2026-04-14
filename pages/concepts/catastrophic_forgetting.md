# 灾难性遗忘（Catastrophic Forgetting）

_最后更新：2026-04-14_

## 概述  
灾难性遗忘指神经网络在学习新任务时**急剧丢失旧任务知识**的现象，在大模型持续预训练（Continual Pre-training）中尤为突出，表现为下游任务性能断崖式下降（如MMLU↓15%），是增量学习的核心挑战。

## 详细内容  

### 产生机制（《百面大模型》Ch.2.5）  
- **权重覆盖假说**：新数据梯度方向与旧数据梯度正交，导致参数更新覆盖旧知识对应权重；  
- **表征坍缩**：模型将新领域token（如代码符号）强行映射到原有语义空间，破坏原有分布（如“def”从Python关键字变为普通名词）；  
- **实证证据**：在Llama-2-7B上用CodeParrot数据持续预训练10k步后，CommonsenseQA准确率从72.3%→54.1%，而代码补全准确率仅从12.1%→18.7%。

### 缓解策略有效性排序  
| 方法 | 原理 | MMLU恢复率 | 计算开销 |  
|------|------|-------------|------------|  
| **Elastic Weight Consolidation (EWC)** | 对重要参数施加二次惩罚 | +8.2% | ★★★☆ |  
| **Experience Replay** | 重放旧数据子集（10%比例） | +12.7% | ★★☆ |  
| **Progressive Neural Networks** | 冻结旧列，新增列适配新任务 | +15.3% | ★★★★ |  
| **Parameter-Efficient Tuning (LoRA)** | 仅更新低秩适配器，主干冻结 | +18.9% | ★☆ |  

### 工程落地建议  
- **首选LoRA**：在持续预训练中，对所有Linear层注入LoRA（r=8, α=16），可将遗忘率压制在≤2%（《百面大模型》p.47）；  
- **数据混合黄金比例**：新旧数据按 7:3 混合，优于纯新数据或纯回放；  
- **监控指标**：除MMLU外，必须跟踪`perplexity on old domain`（如WikiText-103）与`token entropy variance`（表征多样性）。

## 相关页面  
[[concepts/continual_learning]]  
[[concepts/lora]]  
[[concepts/parameter_efficient_finetuning]]  
[[models/llama]]  
[[trends/ai_reliability_engineering]]  

## 来源  
《百面大模型》，第2.5节“持续预训练与灾难性遗忘”，pp. 47–48；Kirkpatrick et al., “Overcoming catastrophic forgetting in neural networks”, PNAS 2017