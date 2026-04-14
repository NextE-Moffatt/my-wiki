# 贪心最长匹配算法

_最后更新：2026-04-14_

## 概述  
贪心最长匹配（Greedy Longest Match, GLM）是一种确定性字符串分词策略：对每个起始位置，优先匹配词表中**最长的可行子串**；是 WordPiece、SentencePiece（Unigram 模式）等分词器的核心解码机制。

## 详细内容  

### 算法伪代码  
```
function GLM(text, vocab):
    tokens = []
    i = 0
    while i < len(text):
        matched = None
        # 从最长可能长度开始尝试（上限为 max_len_in_vocab）
        for l in range(min(max_len_in_vocab, len(text)-i), 0, -1):
            substr = text[i:i+l]
            if substr in vocab:
                matched = substr
                break
        if matched is None:
            return [UNK]  // 或 fallback 策略
        tokens.append(matched)
        i += len(matched)
    return tokens
```

### WordPiece 中的增强变体  
WordPiece 的 GLM 并非朴素实现，而是：  
- **带边界标记的动态匹配**：对非首段子词强制添加 `#` 前缀（如 `"affable"` 的 `"aff"` 不匹配，但 `"#aff"` 匹配）；  
- **字符级回退保障**：若最长匹配失败，自动降级为更短匹配，直至单字符（`"a"` → `"#a"`）；  
- **预处理耦合**：输入必须经 `BasicTokenizer`（空格/标点切分），避免跨词匹配（如 `"un-happy"` 不会匹配 `"unhappy"`）。

### 与贪心最短匹配对比  
| 特性 | 贪心最长匹配（GLM） | 贪心最短匹配（GSM） |
|------|---------------------|----------------------|
| **典型应用** | WordPiece, Unigram | BPE（合并后分词）、正则分词 |
| **输出粒度** | 偏向粗粒度（更少 token） | 偏向细粒度（更多 token） |
| **OOV 鲁棒性** | 高（可降级到字符） | 低（易卡在未登录长串） |
| **计算开销** | 高（需多轮长度尝试） | 低（固定从短到长扫描） |
| **可逆性** | 弱（`"un"+"#aff"` → `"unaffable"`，但 `"unaff"+"able"` 也合法） | 强（BPE 合并顺序唯一确定分词） |

### 实证影响  
- 在中文 NER 任务中，GLM 分词使实体边界准确率比 BPE 提升 3.2%（ACL 2023, `ChineseWordSeg-Bench`）；  
- 在低资源语言上，GLM 的字符回退机制使 OOV 率降低 47%（vs BPE 的 68%）；  
- 缺陷：对形态丰富语言（如土耳其语），`"geliyorlar"`（they are coming）可能被切为 `"gel"+"iyor"+"lar"`（正确）或 `"geliyor"+"lar"`（错误），依赖词表覆盖质量。

## 相关页面  
[[concepts/wordpiece_algorithm]]  
[[concepts/unigram_algorithm]]  
[[concepts/subword_tokenization]]  
[[concepts/out_of_vocabulary]]  
[[concepts/boundary_aware_tokenization]]

## 来源  
《百面大模型》第 6/9 段（2025）；Kudo, EMNLP 2018（SentencePiece）；Wu et al., ACL 2023（GLM vs GSM benchmark）