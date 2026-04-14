# Pre-Norm 与 Post-Norm

_最后更新：2026-04-14_

## 概述  
Pre-Norm（前置归一化）与Post-Norm（后置归一化）指归一化层在Transformer残差块中的位置差异：Pre-Norm将LayerNorm置于子层（Attention/FFN）之前，Post-Norm置于之后；当前主流模型（如LLaMA、GPT-3）均采用Pre-Norm。

## 详细内容  

### 结构定义与梯度特性  
- **Post-Norm（原始Transformer）**：  
  $x_{\text{out}} = \text{SubLayer}(\text{LayerNorm}(x_{\text{in}})) + x_{\text{in}}$  
  → 梯度流经残差连接时**未归一化**，深层易梯度爆炸/消失；  
- **Pre-Norm（现代标准）**：  
  $x_{\text{out}} = \text{SubLayer}(x_{\text{in}}) + x_{\text{in}}, \quad \text{then } \text{LayerNorm}(x_{\text{out}})$  
  → 残差连接输入始终为**归一化后向量**，梯度更平滑。

### 实验对比数据（《百面大模型》Ch.6.10.2）  
| 指标 | Post-Norm（12层） | Pre-Norm（12层） |  
|------|-------------------|-------------------|  
| 训练稳定性（loss震荡标准差） | 0.082 | 0.019 |  
| 最大可训练层数（相同lr） | ≤16 | ≥32 |  
| 收敛速度（epoch to 2.5 ppl） | 24 | 18 |  
| 推理时Norm开销 | +2×（每层2次LN） | +1×（每层1次LN） |  

### 工程实践建议  
- **必须Pre-Norm的场景**：模型深度 > 24层、使用AdamW优化器、学习率 > 3e-4；  
- **Post-Norm残留价值**：在浅层模型（≤6层）或教学演示中仍可使用，因其结构更直观；  
- **混合方案**：部分模型（如T5）采用Encoder-PreNorm + Decoder-PostNorm，但已非主流。

## 相关页面  
[[concepts/layer_norm]]  
[[concepts/transformer_architecture]]  
[[models/llama]]  
[[models/gpt]]  
[[concepts/residual_connection]]  

## 来源  
《百面大模型》，第6.10节“归一化模块位置的影响”，pp. 184–186；Wang et al., “On Layer Normalization in the Transformer Architecture”, ICML 2021