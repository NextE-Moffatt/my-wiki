# errdetect — Python Toolkit for LLM Error Detection

_最后更新：2026-04-10_

## 概述  
`errdetect` 是一个开源 Python 工具库（PyPI: `errdetect==0.4.2`），提供即插即用的 LLM 错误检测模块，原生支持 SEEED 模型、自反射链（self-reflection chains）及软簇可视化。

## 详细内容  
核心功能：  
- `SEEEDDetector`: 加载 Hugging Face 格式 SEEED 模型，支持 CPU/GPU 推理，内置批处理与置信度校准；  
- `SelfReflectPipeline`: 封装 Llama-3-8B-Instruct 的 self-reflection prompt template（含 [[self_reflection]] 最佳实践）；  
- `ClusterExplorer`: 交互式 Jupyter widget，可视化软簇权重热力图与原型语义（需加载 `seeed-prototypes.json`）；  
- `DialErrorsEvaluator`: 与 [[hf_datasets_dialerrors]] v2.1 对齐的评估脚本，输出 per-error-type F1 与 OOD gap 分析。  

部署友好：  
- Docker image `ghcr.io/ukp/errdetect:0.4.2-cpu`（<300MB）；  
- 支持 LangChain / LlamaIndex 集成钩子（`errdetect.langchain` submodule）。

## 相关页面  
[[models/seeed]]  
[[concepts/self_reflection]]  
[[concepts/soft_clustering]]  
[[tools/hf_datasets_dialerrors]]  
[[trends/ai_reliability_engineering]]

## 来源  
百面大模型.pdf（Appendix D “Tooling Ecosystem”, pp. 155–158）；errdetect GitHub README v0.4.2 (2026-03-22)