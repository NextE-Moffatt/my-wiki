# LoRA

_最后更新：2026-04-14_

## 概述  
LoRA（Low-Rank Adaptation）是一种 PEFT（Parameter-Efficient Fine-Tuning）方法，通过在预训练权重旁注入低秩分解矩阵（$A \in \mathbb{R}^{d \times r}, B \in \mathbb{R}^{r \times d}$），冻结原权重，仅训练 $A,B$，实现高效微调（p. 273，★★★☆☆）。

## 详细内容  
### 设计思路与流程（11.1.1–11.1.2）  
- **核心假设**：预训练模型的权重更新 $\Delta W$ 具有低内在秩（$r \ll d$）  
- **实现流程**：  
  1. 选定目标模块（通常为 Q/V 投影层）  
  2. 初始化 $A \sim \mathcal{N}(0, \sigma^2),\ B = 0$，其中 $\sigma = \sqrt{2/r}$（He 初始化）  
  3. 前向：$h = Wx + BAx$，其中 $W$ 冻结，$BA$ 为增量  
  4. 合并：推理时融合 $W' = W + BA$，零额外延迟  
- **秩选择**：$r=8$ 时在 Alpaca 上达 SFT 98.2% 效果；$r=64$ 时达 99.7%，但参数量增 8×  

### 与全参数微调对比（11.3）  
| 维度         | LoRA ($r=8$) | 全参数微调 |  
|--------------|--------------|------------|  
| 可训练参数量 | 0.12%        | 100%       |  
| 显存占用     | ↓ 65%        | baseline   |  
| 训练速度     | ↑ 2.3×       | baseline   |  
| 最终效果     | MMLU ↓0.8%   | baseline   |  

## 相关页面  
[[concepts/peft]] [[models/bert]] [[models/gpt]] [[concepts/contrastive_learning]]

## 来源  
《百面大模型》，第 11.1 节 “LoRA”，pp. 273–274