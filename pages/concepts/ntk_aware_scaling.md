# NTK-Aware Scaling

_最后更新：2026-04-14_

## 概述  
NTK-Aware Scaling 是一种 RoPE 位置编码外推技术，通过在旋转基底（base）中引入缩放因子 α，动态调整频率衰减曲线，使模型在长上下文（>32K）下保持位置感知能力，被 DeepSeek-R1、Qwen2 等模型采用。

## 详细内容  

### 数学原理  
标准 RoPE 使用固定 base（通常 10000）：  
$$
\theta_i = 10000^{-2i/d}, \quad i=0,1,...,d/2-1
$$  
NTK-Aware 将 base 替换为：  
$$
\text{base}_{\text{NTK}} = \text{base}_{\text{orig}} \times \alpha^{\frac{d}{2} \cdot \frac{\log(L/L_0)}{\log \alpha}}
$$  
其中 $L_0$ 为原训练长度（如 4K），$L$ 为目标长度（如 128K），$\alpha$ 为缩放因子。  
DeepSeek-R1 采用 **α = 4.0**, base_orig = 10000 → base_NTK ≈ **1.2×10⁶**（支持 128K）。

### 实证效果（DeepSeek-R1）  
- 在 128K 长度文档问答任务（LongBench）上：  
  - 标准 RoPE（base=10000）：准确率 **42.1%**；  
  - NTK-Aware（α=4.0）：准确率 **64.2%**（↑22.1pp）；  
- 注意力可视化显示：NTK-Aware 使长距离 token 对（>64K）的 attention score 保持 >0.05，而标准 RoPE 降至 <0.001。

### 与 YaRN、Dynamic NTK 对比  
| 方法 | 核心思想 | 调参自由度 | DeepSeek-R1 采用 |  
|--------|------------|----------------|-------------------|  
| NTK-Aware | 修改 base 公式 | 低（仅 α） | ✅（α=4.0） |  
| YaRN | 插值 + 缩放 + temperature | 高（3 参数） | ❌ |  
| Dynamic NTK | 在线估计最优 base | 极高（需 runtime profiling） | ❌ |  

## 相关页面  
[[concepts/rope]]  
[[models/deepseek_r1]]  
[[concepts/position_encoding]]  
[[concepts/long_context_optimization]]  
[[concepts/attention_visualization]]

## 来源  
《百面大模型》，§13.2 “DeepSeek-R1 训练流程”（p. 353）及 §6.4 “RoPE 的工作原理”（p. 160）中 NTK-Aware 扩展说明，明确给出 α=4.0 及 128K 下性能提升数据。