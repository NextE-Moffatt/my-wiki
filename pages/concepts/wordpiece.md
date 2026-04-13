# WordPiece

_最后更新：2026-04-13_

## 概述  
WordPiece 是一种基于**最大似然估计**的子词分词算法，通过 EM 迭代选择使语料对数似然增益最大的子词对进行合并；其核心目标是**最大化训练语料在当前词表下的概率**。

## 详细内容  

### 算法原理（依据《百面大模型》第34页对比说明）  
- 初始词表：所有 Unicode 字符 + 常见标点；  
- 每轮迭代：  
  - 枚举所有可能的相邻子词对 `(a,b)`；  
  - 计算将 `a+b` 加入词表后，语料对数似然的**理论增益**（需估计新词元的出现概率）；  
  - 选择使似然增益最大的 `(a,b)` 合并，并加入词表；  
- 终止条件：词表达目标大小（如 30k）或增益低于阈值。  

> ✅ 关键区别：BPE 是**频率驱动**（count-based），WordPiece 是**概率驱动**（likelihood-based）。前者选 `max freq(a,b)`，后者选 `argmax Δlog P(corpus)`。

### 与 BPE 的实践差异  
- **未登录词处理**：WordPiece 使用 `##` 前缀标记子词（如 `playing` → `play` + `##ing`），显式区分词首/词中；BPE 无此约定，依赖合并顺序隐式建模。  
- **分词确定性**：WordPiece 分词需**最大正向匹配（MaxMatch）** —— 每次取最长可能子词；BPE 分词为**贪心左优先合并**，二者在边界 case 可能不同（如 `lowers`：BPE 可能切为 `low`+`ers`，WordPiece 可能为 `lower`+`##s`）。  
- **工业部署**：BERT 原始实现使用 WordPiece（`bert-base-uncased-vocab.txt` 含 `##` 标记）；RoBERTa 改用 BPE（无 `##`，更简洁）。

### 性能影响  
- WordPiece 在**形态丰富语言**（如德语、土耳其语）上更优，因其能更好捕获词形变化规律；  
- BPE 在**低资源语言**或**混合脚本文本**（如中英混排）中更鲁棒，因频次统计对噪声更不敏感。

## 相关页面  
[[concepts/subword_tokenization]]  
[[concepts/bpe]]  
[[models/bert]]  
[[models/roberta]]  
[[concepts/polysemy_problem]]  

## 来源  
《百面大模型》，第34页，“1.3.2 WordPiece vs BPE”对比段落；术语定义与算法目标引自原文明确陈述。