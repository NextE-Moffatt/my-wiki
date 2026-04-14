# Gutenberg

_最后更新：2026-04-14_

## 概述  
Gutenberg 是一个发布于 2019 年的西方经典文学语料库，收录 28,752 本公版书籍（主要为 19 世纪及更早作品），语言风格古雅、句法严谨，与现代图书（Books3）形成鲜明对比；在 Llama 预训练数据中，Gutenberg 与 Books3 合计占比 4%。

## 详细内容  
据《百面大模型》第 2.1 节，Gutenberg 数据集的关键属性如下：

- **发布时间与规模**：2019 年发布，共 28,752 本书；  
- **内容特征**：  
  - 几乎全部为公版（public domain）作品，以英语为主；  
  - 作者包括莎士比亚、狄更斯、爱默生等，文本具有高度规范化标点、正式语法与丰富修辞；  
  - 与 Books3 的现代口语化、网络化风格形成**时代与语体双重互补**；  
- **在 Llama 中的配比**：与 Books3 合并统计，共占预训练语料 **4%**；  
- **预处理挑战**：  
  - 存在大量古英语拼写（如 “shew” for “show”）、过时标点（如长破折号 —）；  
  - 需专用 normalization pipeline（如拼写标准化、标点归一化）；  
- **建模价值**：提升模型对经典文本的理解能力，增强跨时代语言泛化性，缓解“现代语料偏置”。

该数据集与 `datasets/books3` 页面互为镜像，共同支撑大模型的**历时性语言建模能力**（diachronic language modeling）。

## 相关页面  
[[datasets/books3]]  
[[datasets/bookcorpus]]  
[[concepts/spelling_correction]]  
[[concepts/stemming]]  
[[concepts/lemma_dict_in_embedding_loading]]

## 来源  
《百面大模型》，第 2.1 节 “大模型训练开源数据集”，2025 年出版；含 Gutenberg 发布年份（2019）、规模（28,752）、Llama 配比（4%，与 Books3 合计）。