# Gutenberg

_最后更新：2026-04-13_

## 概述  
Project Gutenberg 是全球首个数字图书馆，成立于1971年，提供超28,752本**公版西方经典文学作品**（主要为1928年前出版），以古英语语法、正式文体与高文学性为特征，是大模型训练中**语言风格多样性与历史语义建模**的关键数据源。

## 详细内容  
- **核心属性**：  
  - 版权状态：全部为 US Public Domain（美国版权法下1928年前出版）；  
  - 语言：92% 英文，其余为德语（3.1%）、法语（2.4%）、西班牙语（1.7%）；  
  - 体裁：小说（61%：狄更斯、奥斯汀、雨果）、非小说（29%：达尔文、亚当·斯密）、诗歌（10%）。  
- **技术适配挑战**：  
  - 古英语拼写与标点（如 `shew`/`colour`/`—` em-dash）需标准化（`spacy` 的 `en_core_web_sm` + 自定义规则）；  
  - 长段落无分句（平均句长 42 字符 vs 现代文本 22 字符），影响位置编码学习；  
  - 缺乏现代实体（如“GPU”、“Transformer”），但提供丰富隐喻与修辞范式。  
- **在 Llama-2 中的定位**：与 Books3 合并计为 **4%** 预训练数据，单独占比约 **1.2%**；控制实验显示：保留 Gutenberg 显著提升模型在 `Literary Analysis` 任务上的 zero-shot 准确率（+8.4%），但对 `Code Generation` 无影响。  
- **对比 Books3**：  
  | 维度 | Gutenberg | Books3 |  
  |------|-----------|--------|  
  | 平均句长 | 42.1 字符 | 21.7 字符 |  
  | 代词密度 | 12.3% (`he/she/they`) | 8.9% |  
  | 技术术语频率 | < 0.01% | 4.2% (`API`, `debug`, `tensor`) |  
  | Temporal bias | Pre-1928 | Post-2000 |

## 相关页面  
[[datasets/books3]] [[models/llama]] [[concepts/historical_language_modeling]] [[tools/spacy]]

## 来源  
《百面大模型》，第2章，第50页（2025）；Llama-2 Technical Report (Meta, 2023)；Project Gutenberg Official Statistics (2023).