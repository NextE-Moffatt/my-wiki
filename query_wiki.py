#!/usr/bin/env python3
"""
Wiki 问答 — 两阶段按需 RAG
  阶段 1：搜 Wiki 页面回答（结构化知识）
  阶段 2：若 AI 判断需要细节 → 自动搜原始文档补充

用法：DASHSCOPE_API_KEY=sk-... python3 query_wiki.py "你的问题"
"""

import os
import re
import sys
import json
import math
from pathlib import Path
from collections import Counter
from openai import OpenAI

# ── 配置 ──
API_KEY  = os.environ.get("DASHSCOPE_API_KEY", "")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL    = "qwen-plus"
EMBED_MODEL = "text-embedding-v3"
EMBED_DIM = 1024

WIKI_DIR  = Path(__file__).parent
PAGES_DIR = WIKI_DIR / "pages"
INDEX_DIR = WIKI_DIR / "index"

MAX_WIKI_PAGES = 8
MAX_CHUNKS     = 6
MAX_CHARS      = 30000


# ── 向量检索 ──

def cosine_sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


def load_index():
    wiki_path = INDEX_DIR / "wiki_index.json"
    chunks_path = INDEX_DIR / "chunks_index.json"
    if not wiki_path.exists():
        return None, None
    with open(wiki_path) as f:
        wiki_index = json.load(f)
    chunks_index = []
    if chunks_path.exists():
        with open(chunks_path) as f:
            chunks_index = json.load(f)
    return wiki_index, chunks_index


def embed_query(client, query):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=[query[:8000]],
        dimensions=EMBED_DIM,
    )
    return response.data[0].embedding


def vector_search(query_embedding, index, top_k):
    scored = []
    for entry in index:
        sim = cosine_sim(query_embedding, entry["embedding"])
        scored.append((sim, entry))
    scored.sort(key=lambda x: -x[0])
    return scored[:top_k]


# ── TF-IDF 降级检索 ──

def tokenize_text(text):
    words = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', text.lower())
    chars = re.findall(r'[\u4e00-\u9fff]', text)
    return words + chars


def tfidf_search(question, pages, top_k):
    q_tokens = tokenize_text(question)
    if not q_tokens:
        return list(pages.items())[:top_k]
    page_tokens = {}
    for path, content in pages.items():
        filename = Path(path).stem.replace("_", " ")
        page_tokens[path] = tokenize_text(filename + " " + filename + " " + content)
    n = len(page_tokens)
    df = Counter()
    for tokens in page_tokens.values():
        for t in set(tokens):
            df[t] += 1
    idf = {t: math.log((n + 1) / (freq + 1)) + 1 for t, freq in df.items()}
    scores = {}
    q_set = set(q_tokens)
    for path, tokens in page_tokens.items():
        tf = Counter(tokens)
        total = len(tokens) or 1
        score = sum(tf[qt] / total * idf.get(qt, 1) for qt in q_set if qt in tf)
        filename_lower = Path(path).stem.replace("_", " ").lower()
        for qt in q_tokens:
            if qt in filename_lower:
                score += 5.0
        scores[path] = score
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return [(path, pages[path]) for path, _ in ranked[:top_k] if scores[path] > 0]


# ── 阶段 1：Wiki 检索 + 回答 ──

def stage1_prompt(question, wiki_results):
    wiki_content = ""
    char_count = 0
    for item in wiki_results:
        if isinstance(item, tuple) and len(item) == 2:
            if isinstance(item[1], dict):
                path, content = item[1]["path"], item[1]["content"]
            else:
                path, content = item
        if char_count + len(content) > MAX_CHARS:
            break
        wiki_content += f"\n=== {path} ===\n{content}\n"
        char_count += len(content)

    return f"""你是一个基于个人 Wiki 知识库的问答助手。

请根据以下 Wiki 页面回答用户问题。

要求：
- 只根据 Wiki 内容回答，不要编造
- 引用 [[页面名]] 标注来源
- 用中文回答，要有深度

**重要**：回答完毕后，请在最后一行输出一个判断标记：
- 如果你认为回答已经完整、不需要更多细节 → 输出 `[COMPLETE]`
- 如果你觉得 Wiki 中缺少具体的数据、公式、实验结果、代码等细节，查阅原始文档可能补充更多信息 → 输出 `[NEED_DETAIL]`，并简要说明需要什么细节

## Wiki 页面
{wiki_content}

## 用户问题
{question}
"""


# ── 阶段 2：原始文档补充 ──

def stage2_prompt(question, stage1_answer, chunk_results):
    chunk_content = ""
    char_count = 0
    for score, entry in chunk_results:
        content = entry["content"]
        source = entry["source"]
        chunk_id = entry["chunk_id"]
        if char_count + len(content) > MAX_CHARS * 0.5:
            break
        chunk_content += f"\n=== {source} [片段 {chunk_id + 1}] ===\n{content}\n"
        char_count += len(content)

    return f"""你是一个知识库问答助手。之前你基于 Wiki 页面给出了一个回答，但需要补充来自原始文档的细节。

## 之前的 Wiki 回答
{stage1_answer}

## 原始文档片段（包含更多细节）
{chunk_content}

## 用户原始问题
{question}

请基于原始文档片段，补充之前回答中缺失的细节（如具体数据、公式、实验结果、代码片段等）。
要求：
- 只补充新信息，不要重复已有内容
- 标注来源 [文档名]
- 如果原始文档中也没有更多细节，说明"原始文档中未找到更多相关细节"
- 用中文回答
"""


def main():
    if len(sys.argv) < 2:
        print("用法：python3 query_wiki.py \"你的问题\"")
        print("示例：python3 query_wiki.py \"什么是注意力机制？\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    if not API_KEY:
        print("错误：请设置 DASHSCOPE_API_KEY 环境变量")
        sys.exit(1)

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # 加载索引
    wiki_index, chunks_index = load_index()

    # ── 阶段 1：Wiki 检索 ──
    if wiki_index:
        q_embedding = embed_query(client, question)
        wiki_results = vector_search(q_embedding, wiki_index, MAX_WIKI_PAGES)
        print(f"📚 Wiki 检索（{len(wiki_index)} 页）→ 命中 {len(wiki_results)} 页：")
        for score, entry in wiki_results:
            print(f"  {score:.3f}  {entry['path']}")
    else:
        print("⚠️  无向量索引，使用关键词检索")
        pages = {}
        for md in PAGES_DIR.rglob("*.md"):
            rel = str(md.relative_to(WIKI_DIR))
            pages[rel] = md.read_text()
        wiki_results = tfidf_search(question, pages, MAX_WIKI_PAGES)
        q_embedding = None
        print(f"📚 Wiki 检索 → 命中 {len(wiki_results)} 页")

    print(f"\n问题：{question}\n")
    print("─" * 50)
    print("📖 阶段 1：基于 Wiki 知识回答\n")

    prompt1 = stage1_prompt(question, wiki_results)
    response1 = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt1}],
        max_tokens=4000,
        temperature=0.2,
    )
    stage1_answer = response1.choices[0].message.content

    # 检查是否需要补充细节
    needs_detail = "[NEED_DETAIL]" in stage1_answer

    # 清理标记后输出
    clean_answer = stage1_answer.replace("[COMPLETE]", "").replace("[NEED_DETAIL]", "").strip()
    # 提取 NEED_DETAIL 后面的说明
    detail_hint = ""
    if needs_detail:
        parts = stage1_answer.split("[NEED_DETAIL]")
        if len(parts) > 1:
            detail_hint = parts[1].strip()

    print(clean_answer)

    # ── 阶段 2：按需检索原始文档 ──
    has_chunks = chunks_index and len(chunks_index) > 0

    if needs_detail and has_chunks:
        print(f"\n\n{'─' * 50}")
        print(f"🔍 阶段 2：检索原始文档补充细节")
        if detail_hint:
            print(f"   需要：{detail_hint}")

        # 用问题 + 缺失信息描述做联合检索
        search_query = question + " " + detail_hint if detail_hint else question
        if q_embedding is None:
            q_embedding = embed_query(client, search_query)
        else:
            q_embedding = embed_query(client, search_query)

        chunk_results = vector_search(q_embedding, chunks_index, MAX_CHUNKS)

        print(f"\n📄 原始文档命中 {len(chunk_results)} 个片段：")
        for score, entry in chunk_results:
            preview = entry['content'][:50].replace('\n', ' ')
            print(f"  {score:.3f}  [{entry['source']} #{entry['chunk_id']+1}] {preview}...")

        print()

        prompt2 = stage2_prompt(question, clean_answer, chunk_results)
        response2 = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt2}],
            max_tokens=3000,
            temperature=0.2,
            stream=True,
        )

        for chunk in response2:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n")

    elif needs_detail and not has_chunks:
        print(f"\n\n💡 Wiki 中缺少部分细节，但原始文档索引为空。")
        print(f"   运行 python3 build_index.py 可构建原始文档索引。")
    else:
        print("\n")


if __name__ == "__main__":
    main()
