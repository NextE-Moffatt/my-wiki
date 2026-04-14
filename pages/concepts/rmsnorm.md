# RMSNorm（Root Mean Square Layer Normalization）

_最后更新：2026-04-14_

## 概述  
RMSNorm是一种**省略均值中心化步骤的LayerNorm变体**，仅对输入向量做RMS缩放与仿射变换，被LLaMA、Gemma等模型采用，可降低计算开销约15%且保持数值稳定性。

## 详细内容  

### 数学公式  
对输入 $x \in \mathbb{R}^d$，RMSNorm定义为：  
$$
\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum_{i=1}^d x_i^2 + \epsilon}} \odot \gamma + \beta  
$$  
对比标准LayerNorm：  
$$
\text{LayerNorm}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \odot \gamma + \beta, \quad \mu = \frac{1}{d}\sum x_i, \ \sigma^2 = \frac{1}{d}\sum (x_i - \mu)^2  
$$  
**关键差异**：RMSNorm移除均值 $\mu$ 计算与方差 $\sigma^2$ 中的中心化项，仅依赖二阶矩。

### 性能优势实测（《百面大模型》Ch.6.9.4）  
- **FLOPs降低**：在A100上，RMSNorm比LayerNorm快14.2%（因省去$d$次减法与$d$次乘法）；  
- **显存节省**：无需缓存均值 $\mu$，每层减少 $2 \times d \times \text{sizeof(float)}$ 字节（LLaMA-7B中每层省约1.2MB）；  
- **收敛性**：在相同学习率下，RMSNorm训练loss下降速度与LayerNorm一致，但梯度方差降低18%（因消除均值噪声）。

### 与LayerNorm的适用边界  
| 场景 | LayerNorm | RMSNorm |  
|------|------------|----------|  
| **小批量训练**（batch_size<4） | ✅ 更鲁棒（均值稳定） | ⚠️ RMS易受离群值影响 |  
| **大语言模型**（d>4096） | ❌ 计算开销显著 | ✅ 主流选择（LLaMA/Gemma） |  
| **需要精确控制激活分布** | ✅ 可控均值/方差 | ❌ 仅控制scale |  

## 相关页面  
[[concepts/layer_norm]]  
[[concepts/batch_norm]]  
[[models/llama]]  
[[models/gemma]]  
[[concepts/normalization_layers]]  

## 来源  
《百面大模型》，第6.9.4节“RMSNorm的工作原理”，pp. 184–185；Zhang & Sennrich, “Root Mean Square Layer Normalization”, NeurIPS 2019