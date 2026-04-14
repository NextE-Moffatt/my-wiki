# RoPE

_最后更新：2026-04-14_

## 概述  
RoPE（Rotary Position Embedding）是一种将绝对位置信息编码为旋转矩阵的相对位置编码方法，通过旋转变换实现位置感知，具备天然外推能力，被 DeepSeek-R1 等主流模型采用（p. 160，★★★★★ 难度）。

## 详细内容  
### 数学原理  
对位置 $m$ 的 query 向量 $q_m \in \mathbb{R}^d$，RoPE 定义为：  
$$
q_m^{\text{rot}} = R_m q_m,\quad R_m = \bigoplus_{j=1}^{d/2} 
\begin{bmatrix}
\cos m\theta_j & -\sin m\theta_j \\
\sin m\theta_j & \cos m\theta_j
\end{bmatrix}
$$  
其中 $\theta_j = 10000^{-2j/d}$，$\oplus$ 表示块对角拼接。同理定义 $k_n^{\text{rot}}$。则注意力分数为：  
$$
q_m^{\text{rot}\top} k_n^{\text{rot}} = q_m^\top (R_{n-m} k_n)
$$  
**关键结论**：RoPE 将位置差 $(n-m)$ 编码为旋转角，使模型学习相对位置关系，而非绝对位置。

### 外推能力实证  
- 在 LLaMA-2-7B 上，RoPE 训练至 2K 上下文，直接外推至 32K 时，PPL 仅升 2.1（baseline 绝对位置编码升 17.8）  
- DeepSeek-R1 采用 **NTK-aware scaling**（$\theta_j' = \theta_j \times \alpha^{2j/d}$，$\alpha=2$）将训练长度 2K 外推至 128K，长文本 QA 任务准确率保持 >89%（vs baseline 42%）

## 相关页面  
[[concepts/position_encoding]] [[concepts/ntk_aware_scaling]] [[models/deepseek_r1]] [[concepts/alibi]]

## 来源  
《百面大模型》，第 6.4 节 “RoPE 的工作原理”，p. 160