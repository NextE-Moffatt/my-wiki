# Books3

_最后更新：2026-04-14_

## 概述  
Books3 是由 Shawn Presser 于 2020 年构建的大规模图书语料库，包含 196,640 本小说与非小说类图书，是 Llama 等大模型预训练的关键文本来源；在 Llama 预训练数据中，Books3 与 Gutenberg 合计占比 4%。

## 详细内容  
依据《百面大模型》第 2.1 节，Books3 的技术细节如下：

- **构建时间与作者**：2020 年，Shawn Presser；  
- **规模**：196,640 本书（远超 BookCorpus 的 11,038 本与 BookCorpus2 的 17,868 本）；  
- **内容构成**：涵盖小说（fiction）与非小说（non-fiction）两大类，题材多样，语言风格现代；  
- **在 Llama 中的配比**：与 Gutenberg 数据合并统计，共占预训练语料的 **4%**；  
- **对比 BookCorpus**：  
  - BookCorpus（2015）：16 类未出版免费书，11,038 本；  
  - BookCorpus2（扩充版）：17,868 本；  
  - Books3 规模达 BookCorpus 的 **17.6×**，且更注重版权合规性与文本多样性；  
- **价值**：提供长程依赖建模所需的连贯叙事结构、丰富词汇与复杂句法，弥补网页语料（Common Crawl）碎片化缺陷。

该数据集与 `datasets/gutenberg` 形成互补：Books3 代表现代文学，Gutenberg 代表西方经典文学（28,752 本，19 世纪前作品为主）。

## 相关页面  
[[datasets/gutenberg]]  
[[datasets/bookcorpus]]  
[[datasets/webtext]]  
[[models/llama]]  
[[concepts/data_cleaning]]

## 来源  
《百面大模型》，第 2.1 节 “大模型训练开源数据集”，2025 年出版；含 Books3 构建者、年份、规模（196,640）、Llama 配比（4%，与 Gutenberg 合计）。