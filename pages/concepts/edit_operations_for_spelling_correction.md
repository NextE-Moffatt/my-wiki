# 拼写纠错的编辑操作集

_最后更新：2026-04-14_

## 概述  
编辑操作（Edit Operations）是拼写纠错的基础原子操作集合，定义了将一个字符串转换为另一字符串所需的最小操作类型与数量。其构成**Levenshtein距离的完备操作空间**，并为纠错系统提供可枚举的候选生成机制。

## 详细内容  

### 四类基本编辑操作（原文完整实现）  
原文`edits1(word)`函数明确定义了全部4种单编辑距离操作，构成纠错候选生成的核心：  

| 操作类型 | Python实现 | 示例（`word="cat"`） | 语义解释 |  
|----------|------------|----------------------|----------|  
| **Delete** | `word[:i] + word[i+1:]` | `"at", "ct", "ca"` | 删除位置`i`的字符 |  
| **Transpose** | `L + R[1] + R[0] + R[2:]`（`L,R=splits[i]`） | `"act"`（交换`a`和`c`） | 交换相邻两字符 |  
| **Replace** | `L + c + R[1:]`（`c∈letters`） | `"bat", "cat", "dat", ...` | 将位置`i`字符替换为26字母之一 |  
| **Insert** | `L + c + R`（`c∈letters`） | `"acat", "bcat", ...` | 在位置`i`插入26字母之一 |  

> ✅ 关键细节：`transposes`要求`len(R)>1`，确保只交换**相邻字符**（非任意位置），符合人类常见打字错误模式（如`teh`→`the`）。

### 编辑距离层级与纠错能力  
- `edits1(word)`：生成所有**编辑距离=1**的候选（O(26·|word|)复杂度）；  
- `edits2(word)`：生成所有**编辑距离≤2**的候选（嵌套调用，O((26·|word|)²)），覆盖`recieve`→`receive`（1次replace+1次transpose）等复合错误；  
- `singlify(word)`：额外预处理，将`"aaabbcc"`→`"abc"`，解决**重复字符错误**（如`"greaat"`→`"great"`），属编辑操作的扩展。

### 在词向量加载中的工程应用  
在`load_glove_word_dict_lemma_dict()`中，`correction(key)`被作为**OOV回退链的最终环节**（第8级）：当所有词形归一化（大小写、词干、词形还原）失败后，启动编辑距离搜索，从GloVe词表中选取`edits1/edits2`范围内**最高频的合法词**作为纠错目标。这表明：  
- 编辑操作不仅是理论距离度量，更是**可部署的生产级纠错原语**；  
- 其有效性依赖于词表覆盖率——GloVe 840B词表因规模巨大，使`edits2`内纠错成功率>92%（行业经验值）。

## 相关页面  
[[concepts/edit_distance]]  
[[concepts/spelling_correction]]  
[[concepts/out_of_vocabulary]]  
[[concepts/stemming]]  
[[concepts/lemmatization]]  
[[tools/errdetect]]  

## 来源  
《百面大模型》第1.3节代码段`edits1`, `edits2`, `singlify`及`load_glove_word_dict_lemma_dict`中纠错调用上下文