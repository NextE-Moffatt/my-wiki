# Soft Clustering

_最后更新：2026-04-10_

## 概述  
软聚类是一种允许样本以概率形式隶属多个簇的无监督学习方法，相较于硬聚类（如 K-means），更契合真实世界中错误语义的模糊性与重叠性。

## 详细内容  
在 LLM 错误检测中，软聚类被用于建模错误空间的连续性：  
- SEEED（[[models/seeed]]）使用 Gumbel-Softmax 参数化 16 维簇分布，每个维度对应一个可解释错误原型（prototype），如 “temporal_inconsistency” 或 “pragmatic_violation”；  
- 簇原型通过 contrastive clustering loss 学习：拉近同类错误样本的簇概率分布，推远异类；  
- 关键优势：支持 zero-shot 扩展——新增错误类型时，仅需注入新原型向量，无需重训全模型（对比硬聚类需重新分配所有样本）。  

与相关概念区别：  
- [[attention_mechanism]] 关注 token 间关系建模；软聚类关注 *样本级语义结构* 建模；  
- [[scaling_computation]] 提供算力基础，而软聚类提供 *高效利用算力的归纳偏置* —— 小数据下即可泛化（见 [[search_and_learning]]）。

## 相关页面  
[[models/seeed]]  
[[concepts/error_detection_in_llms]]  
[[concepts/ood_generalization]]  
[[concepts/search_and_learning]]  
[[papers/towards_automated_error_discovery]]

## 来源  
百面大模型.pdf（Section 2.4 “Beyond Hard Boundaries: Soft Structures in Error Space”, pp. 28–31）；SEEED Appendix C