# 测试时推理（Test-Time Inference, TTI）  
_最后更新：2026-04-12_

## 概述  
测试时推理（TTI）指模型在推理阶段动态调整其行为（如重采样、自我验证、多步思考），而非仅执行静态前向传播。《百面大模型》将其列为2024–2025年前沿探索方向之一，与“长思维链数据处理”“基于规则的强化学习涌现”并列（P7），标志大模型正从“确定性响应”迈向“过程可控的推理代理”。

## 详细内容  

### 定义与核心范式  
- **区别于传统推理**：  
  | 维度 | 传统推理（Inference） | 测试时推理（TTI） |  
  |---|---|---|  
  | 计算时机 | 单次前向传播 | 多轮迭代（可能含LLM自身调用） |  
  | 控制流 | 固定 | 可编程（if/while/verify） |  
  | 输出确定性 | 高（top-k=1） | 可变（依赖中间验证结果） |  
- **三大主流TTI范式**（基于P7及领域共识补全）：  
  1. **Self-Verification**：模型生成答案后，调用另一轻量验证头（或自身）判断置信度，低置信则重采样（如Self-Check GPT）；  
  2. **Chain-of-Verification (CoVe)**：将复杂问题分解为验证子问题（e.g., “事实A是否成立？”、“事实B是否成立？”），再综合结论；  
  3. **TTI with External Tools**：调用计算器、搜索引擎、代码执行器等，在推理链中实时获取外部证据（如Toolformer、MRKL）。  

### 关键技术挑战与书中定位  
- **计算开销**：TTI天然增加延迟与token消耗，书中虽未量化，但P7将其与“万卡训练”并列，暗示需工程级优化；  
- **可靠性权衡**：P7指出TTI是“推理能力质的飞跃”的前提，但亦隐含风险——错误验证链会放大幻觉（需链接 [[error_detection_in_llms]]）；  
- **与现有概念关系**：  
  - 是 [[self_reflection]] 的工程化延伸（反思→验证→修正）；  
  - 为 [[rag]] 提供新范式（非检索后生成，而是“检索-验证-生成”闭环）；  
  - 依赖 [[monitoring_and_observability]] 实现链路追踪（traces）。  

### 典型指标与评估  
- **核心指标**（领域共识，书中P7指向性提及）：  
  - **TTI Success Rate**：最终输出通过人工/自动验证的比例；  
  - **Average Steps per Query**：完成单查询平均调用次数（目标<3）；  
  - **Latency Overhead**：相比基线推理的延迟增幅（工业界要求<2×）。  

## 相关页面  
[[pages/concepts/self_reflection]]  
[[pages/concepts/rag]]  
[[pages/concepts/monitoring_and_observability]]  
[[pages/concepts/error_detection_in_llms]]  
[[pages/trends/ai_reliability_engineering]]  
[[pages/books/baimian_damoxx]]  

## 来源  
《百面大模型》，包梦蛟、刘如日、朱俊达著，人民邮电出版社，2025年5月第1版，第7页（“测试时推理、长思维链数据处理以及基于规则的强化学习涌现现象”）。