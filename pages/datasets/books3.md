# Books3

_最后更新：2026-04-13_

## 概述  
Books3 是由 Shawn Presser 于2020年发布的大型开源图书语料集，包含196,640本小说与非小说类电子书，以**现代叙事风格与常识密度**著称，是 Llama 系列模型中与 Gutenberg 形成互补的“当代知识”支柱。

## 详细内容  
- **构成与来源**：  
  - 来源：Z-Library 镜像、Library Genesis（LibGen）等影子图书馆的公开镜像；  
  - 类型分布：小说（58%：科幻、奇幻、言情、推理）、非小说（42%：计算机、心理学、经济学、自我提升）；  
  - 格式：PDF → `pdfplumber` 提取文本，后经 OCR 校验（对扫描版 PDF 使用 `Tesseract`）；  
  - 清洗：移除页眉页脚、目录、版权声明、重复章节（MD5 段落哈希去重）。  
- **规模与特征**：  
  - 总文本量：**127 GB**（UTF-8），平均书籍长度 642 KB；  
  - 语言：99.1% 英文，其余为西班牙语（0.5%）、法语（0.3%）；  
  - 关键优势：高密度常识（"how to debug Python code"）、长程叙事连贯性、对话真实感（vs Gutenberg 的古英语句法）。  
- **在 Llama-2 中的作用**：与 Gutenberg（经典文学）合并计为 **4%** 预训练数据，其中 Books3 贡献约 2.8%，Gutenberg 贡献 1.2%；消融实验表明移除 Books3 导致模型在 MMLU 子集 `Humanities` 分数下降 3.2%，但在 `Computer Science` 下降达 5.7%（凸显其技术文本价值）。  
- **伦理争议**：因来源涉及版权灰色地带，Llama-2 技术报告未公开 Books3 具体子集，仅以“Books3/Gutenberg mixture”统称。

## 相关页面  
[[datasets/gutenberg]] [[models/llama]] [[concepts/commonsense_reasoning]] [[tools/pdfplumber]] [[tools/tesseract]]

## 来源  
《百面大模型》，第2章，第50页（2025）；Llama-2 Technical Report (Meta, 2023)；Presser, S. "Books3: A Large-Scale Dataset of Modern Books", arXiv:2005.14165 (2020).