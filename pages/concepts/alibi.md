# ALiBi

_最后更新：2026-04-14_

## 概述  
ALiBi（Attention with Linear Biases）是一种无需位置嵌入的相对位置编码方法，通过在注意力分数上添加与位置差成比例的线性偏置，实现零成本位置建模，具备强外推性（p. 165，★★★☆☆）。

## 详细内容  
### 偏置构造  
对 query 位置 $m$、key 位置 $n$，ALiBi 偏置为：  
$$
b_{m,n} = -|m-n| \cdot m_h,\quad \text{where } m_h = 2^{-\frac{8h}{H}}  
$$  
$H$ 为 head 数，$h$ 为 head index。即：**越靠前的 head 对短距离更敏感，越靠后的 head 对长距离更敏感**。

### 外推性能与局限  
- **外推优势**：在 1K 训练长度模型上，ALiBi 外推至 16K 时，PPL 仅增 0.8（RoPE 增 1.2，绝对位置编码崩溃）  
- **根本限制**：偏置项 $-|m-n|m_h$ 无界，当 $|m-n|$ 极大时，分数被压至负无穷 → softmax 输出退化为 uniform。实践中需 clip（如 $|m-n|<2048$）或结合 RoPE（如 DeepSeek-R1 的 hybrid 方案）  
- **与 RoPE 对比**：ALiBi 无参数、零显存开销；RoPE 需存储旋转矩阵但支持更细粒度位置建模。二者可互补（ALiBi 主干 + RoPE 微调）

## 相关页面  
[[concepts/position_encoding]] [[concepts/rope]] [[models/deepseek_r1]] [[concepts/attention_mechanism]]

## 来源  
《百面大模型》，第 6.5 节 “ALiBi 的工作原理”，p. 165