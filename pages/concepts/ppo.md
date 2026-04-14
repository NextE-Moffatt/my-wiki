# PPO（Proximal Policy Optimization）

_最后更新：2026-04-14_

## 概述  
PPO 是大模型强化学习对齐阶段最主流的策略优化算法，通过带裁剪（clipping）的 surrogate objective 保障每次更新的 KL 散度有界，兼顾训练稳定性与策略改进幅度。

## 详细内容  
PPO 的核心 surrogate loss 定义为：  
$$
\mathcal{L}^{\text{CLIP}}_{\text{PPO}}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) \hat{A}_t,\; \text{clip}(r_t(\theta), 1-\varepsilon, 1+\varepsilon) \hat{A}_t \right) \right]
$$  
其中：
- $r_t(\theta) = \frac{p_\theta(a_t|s_t)}{p_{\theta_{\text{old}}}(a_t|s_t)}$ 为概率比；
- $\hat{A}_t$ 为广义优势估计（GAE），$\hat{A}_t = \sum_{l=0}^\infty (\gamma \lambda)^l \delta_{t+l}$，$\delta_{t} = r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t)$；
- $\varepsilon$ 为裁剪范围（典型值 0.1–0.2）；
- $V_\phi$ 为 Critic 网络（通常与 Actor 共享底层 Transformer，独立 head 输出标量价值）。

据《百面大模型》第 4 章 4.4 节，PPO 训练稳定性优化实践包括：
- **监控指标**：每 step 记录 `ratio_clip_frac`（被裁剪的比例）、`kl_div`（当前策略 vs old 策略 KL）、`entropy`（策略熵）；当 `ratio_clip_frac > 0.3` 或 `kl_div > 0.05` 时需降低 learning rate 或增大 `ε`；
- **梯度处理**：全局梯度裁剪（`max_norm=0.5`）+ 损失标准化（batch 内 loss 减均值除标准差）；
- **初始化优化**：Actor 与 Critic 的 final layer 初始化采用 `orthogonal(0.01)`，避免初始高方差价值估计导致策略震荡。

PPO 的主要瓶颈在于通信与计算开销：单次完整训练需至少 3 次模型前向（actor rollout、critic value、reward model），且 rollout batch size 通常需 ≥ 64 才保证优势估计可靠性，显存占用为 DPO 的 2.8×（同参数量下，见第 12.3 节 FlashAttention 加速上下文）。

## 相关页面  
[[dpo]] [[reinforcement_learning_for_llms]] [[reward_modeling]] [[gae]] [[kl_divergence]] [[flashattention]] [[sft]]

## 来源  
《百面大模型》，第 4 章 4.2、4.4 节（pp. 88–102），2025 年出版