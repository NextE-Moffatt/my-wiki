# Decoder-Only 架构

_最后更新：2026-04-14_

## 概述  
Decoder-only 架构是仅含 Transformer 解码器堆叠的模型结构，采用单向（因果）注意力与自回归语言建模（causal LM）目标训练，是当前开源大模型（Llama、GPT 系列）的主流选择，原生支持高质量文本生成与上下文学习（in-context learning）。

## 详细内容  
依据《百面大模型》第 1.8 节，decoder-only 架构的核心技术规范与实证优势如下：

- **注意力机制**：严格因果掩码（causal mask），位置 $i$ 仅能 attend to $j \leq i$，保障生成过程的时序一致性；  
- **训练目标**：最大化自回归概率 $P(w_i \mid w_1,\dots,w_{i-1})$，即 causal LM；  
- **零样本/少样本能力基础**：  
  - 零样本推断形式化为 $P(y \mid x; \theta_{\text{origin}})$，无需任何参数更新；  
  - 少样本推断为 $P(y \mid \text{example}_1,\dots,\text{example}_e, x; \theta_{\text{origin}})$，通过拼接示例构建 prompt；  
  - 书中以中英翻译为例（“苹果很美味。→ The apple is very nice.”），证实其在未见任务上可直接泛化；  
- **工业部署事实**：Llama、GPT-2/3/4、Qwen、DeepSeek 等全部采用此架构；Llama 预训练数据中，C4 占 15%、Wikipedia 占 4.5%、Books3+Gutenberg 占 4%，印证其对大规模、多样化文本的强适应性；  
- **与 encoder-only 的根本区别**：  
  - 不仅在于“有无解码器”，更在于**注意力方向性**（单向 vs 双向）与**语义内化方式**（隐含于 $\theta$ 中 via ICL vs 显式微调 head）。

书中指出：“为什么近期的大模型架构选型都不约而同地选择了纯解码器架构”是后续章节重点，暗示其已成为生成式 AI 的**事实标准架构**（de facto standard）。

## 相关页面  
[[models/gpt]]  
[[models/llama]]  
[[models/deepseek_r1]]  
[[concepts/decoder_only_architecture]]  
[[concepts/causal_lm]]  
[[concepts/in_context_learning]]  
[[concepts/zero_shot_learning]]  
[[concepts/few_shot_learning]]  
[[models/encoder_only_architecture]]

## 来源  
《百面大模型》，第 1.8 节 “大模型语义建模的典型架构”，2025 年出版；含架构定义、数学形式化（$P(y|x;\theta)$）、实例（Llama 数据配比）、能力论证（翻译示例）。