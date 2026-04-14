# AutoGen

_最后更新：2026-04-14_

## 概述  
AutoGen 是微软开源的多智能体框架（2023），支持可编程、可定制的角色协作范式，核心为 `ConversableAgent` 抽象与基于 LLM 的自动消息协商协议，在 10.6 节被列为工业级智能体实践标杆。

## 详细内容  
### 核心架构  
- **ConversableAgent**：统一基类，封装 `generate_reply()` 方法，支持三种回复模式：  
  1. **LLM-driven**：调用大模型生成回复（默认）  
  2. **Function-driven**：执行注册的 Python 函数（如工具调用）  
  3. **Human-driven**：等待人工输入（用于 human-in-the-loop 场景）  
- **GroupChat & GroupChatManager**：支持 N 个 agent 组成群聊，由 manager 根据 `speaker_selection_method`（如 round-robin、auto-select）调度发言权  
- **Message Protocol**：所有消息为 JSON 格式，含 `role`（user/assistant/function）、`content`、`function_call`（若触发工具）、`name`（调用者名），确保跨 agent 可追溯  

### 工程特性（10.6）  
- **状态持久化**：支持将对话历史序列化为 JSONL，断点续聊；内置 SQLite 后端供长期记忆存储  
- **工具集成**：通过 `register_function()` 注册任意 Python 函数，自动构建 function calling schema；支持异步并发调用（`async_mode=True`）  
- **安全沙箱**：默认禁用 `exec()`/`eval()`，函数执行在受限 `sandbox` 进程中，超时强制 kill（默认 30s）  
- **性能**：在 8-agent 群聊中，平均消息处理延迟 < 120ms（A100 + GPT-4-turbo），吞吐达 8.3 msg/s  

## 相关页面  
[[concepts/self_reflection]] [[concepts/tool_calling]] [[tools/xagent]] [[concepts/monitoring_and_observability]] [[models/gpt]]

## 来源  
《百面大模型》，第 10.6 节 “AutoGen 框架”，p. 266