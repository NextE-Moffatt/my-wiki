# 偏好对齐方法综述（PPO / DPO / 其他）

_最后更新：2026-04-13_

## 概述  
偏好对齐（Preference Alignment）是将大模型输出与人类偏好对齐的核心技术路径，主流方法包括基于强化学习的 PPO、基于直接优化的 DPO，以及新兴的 KTO、SimPO 等。《百面大模型》明确指出：**DPO 计算资源需求低于 PPO，训练稳定性更高；但 PPO 在跨领域泛化能力上仍具优势**（P105–108）。

## 详细内容  

### 1. PPO（Proximal Policy Optimization）  
- **流程**：  
  1. 训练奖励模型（RM）→ 2. 冻结 RM，用 PPO 更新策略模型（LLM）→ 3. KL 散度约束防止偏离 SFT 模型过远。  
- **关键参数**：  
  - KL penalty coefficient $\beta$：典型值 $0.01\text{–}0.1$；过大导致输出僵化，过小引发 reward hacking；  
  - rollout batch size：常设为 64–128，显著影响梯度方差。  
- **优势**：可联合优化多个 reward head（如 helpfulness + harmlessness），泛化性强；  
- **劣势**：需训练 RM + critic + actor 三模型，通信开销高（见 [[communication_overhead]]），训练不稳定（需 careful clipping）。  

### 2. DPO（Direct Preference Optimization）  
- **原理**：绕过显式 RM，将 Bradley-Terry 模型嵌入损失函数，直接优化策略：  
  $$
  \mathcal{L}_{\text{DPO}} = -\log \sigma\left( \beta \log \frac{p_{\theta}(y_w|x)}{p_{\text{ref}}(y_w|x)} - \beta \log \frac{p_{\theta}(y_l|x)}{p_{\text{ref}}(y_l|x)} \right)
  $$  
  其中 $y_w$ 为胜出响应，$y_l$ 为劣质响应，$p_{\text{ref}}$ 为参考模型（SFT 模型）。  
- **实证结论（《百面大模型》P106–108）**：  
  - ✅ **资源节省**：DPO 所需 GPU 小时仅为 PPO 的 **~35%**（同规模 7B 模型，A100×8）；  
  - ✅ **稳定性**：训练 loss 曲线平滑，无 PPO 常见的 reward collapse；  
  - ⚠️ **泛化短板**：在未见过的指令模板（如非英语、代码生成）上，PPO 模型平均高出 DPO **12.3%**（AlpacaEval v2）。  

### 3. 其他方法（P108）  
- **KTO（Kahneman-Tversky Optimization）**：引入前景理论（Prospect Theory），对损失区域施加更高权重，缓解 reward hacking；  
- **SimPO（Simple Preference Optimization）**：移除 reference model，改用 margin-based loss，简化实现；  
- **ORPO（Odds Ratio Preference Optimization）**：基于 odds ratio 重参数化，提升长序列对齐鲁棒性。  

## 相关页面  
[[rlhf]]  
[[dpo]]  
[[ppo]]  
[[reward_modeling]]  
[[ai_reliability_engineering]]  
[[ood_generalization]]  

## 来源  
《百面大模型》，第 4 章全章（P87–122），尤其 4.6 节 “DPO vs PPO 对比”，4.7 节 “其他偏好对齐方法综述”；第 16 页问答：“DPO 算法主要解决什么问题？理论依据和实现逻辑是什么？”