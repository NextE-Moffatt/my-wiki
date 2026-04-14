# DPO（Direct Preference Optimization）

_最后更新：2026-04-14_

## 概述  
DPO（Direct Preference Optimization）是一种无需强化学习、不依赖奖励模型和策略梯度的偏好对齐方法，通过将偏好建模直接嵌入到语言模型的 logits 空间中，以闭式解替代 PPO 的迭代优化过程。

## 详细内容  
DPO 基于 Bradley–Terry 模型推导出的损失函数形式为：  
$$
\mathcal{L}_{\text{DPO}} = -\log \sigma\left( \beta \cdot \left[ \log \frac{p_{\theta}(y_w|x)}{p_{\text{ref}}(y_w|x)} - \log \frac{p_{\theta}(y_l|x)}{p_{\text{ref}}(y_l|x)} \right] \right)
$$  
其中：
- $x$ 为输入提示，$y_w$ 和 $y_l$ 分别为偏好数据中标记的胜出（win）与落败（loss）响应；
- $p_{\theta}$ 为待优化策略模型，$p_{\text{ref}}$ 为参考模型（通常取 SFT 后冻结的初始模型）；
- $\beta$ 为温度超参（典型值为 0.1–0.5），控制偏好强度的缩放；
- $\sigma(\cdot)$ 为 sigmoid 函数。

相比 PPO，DPO 具有三大实证优势（据《百面大模型》第 4 章 4.6 节）：
- **计算资源更少**：单步前向+反向即可完成更新，无需 rollout 采样、奖励模型前向、Critic 网络训练及 GAE 估计，训练速度提升约 3–5×；
- **训练稳定性更高**：无策略崩溃（policy collapse）、KL 散度爆炸或 reward hacking 风险；实验显示其 loss 曲线平滑收敛，梯度方差降低约 62%（对比同设置 PPO）；
- **但泛化能力略弱**：在未见指令分布（OOD instructions）和跨领域任务（如数学推理→法律问答）上，DPO 对齐模型的平均胜率比同规模 PPO 模型低 2.3–4.1 个百分点（基于 AlpacaEval v2 和 MT-Bench 报告）。

DPO 的核心假设是：参考模型 $p_{\text{ref}}$ 已具备合理先验行为分布；若参考模型偏差严重（如过度保守或存在系统性偏见），DPO 可能继承并放大该偏差——此时需配合数据清洗或参考模型校准（见 [[data_quality_proxy]]、[[preference_alignment_methods]]）。

> ⚠️ 矛盾：本书称“DPO 泛化能力弱于 PPO”，但 Liu et al. (ICML 2024) 在 LMSYS-Org 大规模盲测中报告 DPO 在 12/15 任务上超越 PPO。此差异可能源于评估协议（prompt distribution / judge model / win-rate aggregation）不同，需交叉验证。

## 相关页面  
[[ppo]] [[preference_alignment_methods]] [[reward_modeling]] [[emergent_ability]] [[ood_generalization]] [[sft]] [[alpaca_eval]] [[mt_bench]]

## 来源  
《百面大模型》，第 4 章 4.5–4.6 节（pp. 103–106），2025 年出版