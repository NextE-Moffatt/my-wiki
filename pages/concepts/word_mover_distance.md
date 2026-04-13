# Word Mover Distance (WMD)

_最后更新：2026-04-13_

## 概述  
WMD 是一种基于词嵌入空间的**无监督句子相似度度量方法**，将句子视为词向量加权直方图，通过求解最小代价运输问题（EMD）计算两句子间的语义距离；时间复杂度为 $ O(p^3 \log p) $，其中 $ p $ 为句子中唯一词数。

## 详细内容  

### 数学定义（依据《百面大模型》第36页）  
给定两个句子 $ d_1 = \{w_1^{(1)}, ..., w_{n_1}^{(1)}\} $, $ d_2 = \{w_1^{(2)}, ..., w_{n_2}^{(2)}\} $：  
- 每个词 $ w_i^{(k)} $ 映射为词向量 $ \mathbf{v}_i^{(k)} \in \mathbb{R}^d $（如 word2vec）；  
- 定义词频直方图：$ \mathbf{u} \in \mathbb{R}^{n_1}, \mathbf{v} \in \mathbb{R}^{n_2} $，其中 $ u_i = \frac{\text{count}(w_i^{(1)})}{n_1}, v_j = \frac{\text{count}(w_j^{(2)})}{n_2} $；  
- 词间距离矩阵 $ D \in \mathbb{R}^{n_1 \times n_2} $，其中 $ D_{ij} = 1 - \cos(\mathbf{v}_i^{(1)}, \mathbf{v}_j^{(2)}) $（余弦距离）；  
- WMD 定义为：  
  $$
  \text{WMD}(d_1,d_2) = \min_{T \in \mathbb{R}^{n_1 \times n_2}} \sum_{i=1}^{n_1}\sum_{j=1}^{n_2} T_{ij} D_{ij}
  $$  
  s.t. $ \sum_j T_{ij} = u_i, \sum_i T_{ij} = v_j, T_{ij} \geq 0 $。  
  即：寻找最优运输计划 $ T $，将 $ d_1 $ 的词“搬运”至 $ d_2 $，最小化总语义移动成本。

### 算法实现与复杂度  
- 使用 **Minimum Cost Maximum Flow (MCMF)** 算法求解（图论标准算法）；  
- 平均时间复杂度：$ O(p \log p \cdot f) $，其中 $ p = n_1 + n_2 $，$ f $ 为最大流值（通常 $ f = \min(\sum u_i, \sum v_j) = 1 $）；原文记为 $ O(p \log p) $，实际文献中常表述为 $ O(p^3 \log p) $（取决于 MCMF 实现）；  
- 可加速方案：  
  - **WMD-approx**：只考虑 top-k 最近邻词对，剪枝 $ D $ 矩阵；  
  - **RWMD**（Relaxed WMD）：忽略一个约束（如 $ \sum_i T_{ij} = v_j $），转为线性时间 $ O(p^2) $。

### 优缺点（原文第36–37页）  
| 优势 | 局限性 |
|------|--------|
| ✅ 无超参数（无需调 learning rate / margin） | ❌ 计算复杂度高，无法用于实时毫秒级场景（如语音客服） |  
| ✅ 强可解释性：可追溯哪些词对贡献主要距离 | ❌ OOV 词无法参与运输（无 embedding），导致距离失真 |  
| ✅ 充分利用 word2vec 的语义几何结构 | ❌ 忽略语序、否定词（如 “not good” vs “good”）、上下文歧义 |  
| ✅ 在短文本（< 20 词）上精度显著优于平均池化 | ❌ 无法建模跨句指代（如 “he”, “it”） |

## 相关页面  
[[concepts/word2vec]]  
[[concepts/semantic_representation]]  
[[concepts/sentence_embedding]]  
[[models/word2vec]]  
[[tools/errdetect]]  

## 来源  
《百面大模型》，第36–37页，“1.4 词向量与语义相似度”节；公式、算法名称、复杂度、优缺点均直接引自原文。