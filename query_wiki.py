#!/usr/bin/env python3
"""
Wiki 问答 — 基于 wiki 知识库内容回答问题
用法：DASHSCOPE_API_KEY=sk-... python3 query_wiki.py "你的问题"
"""

import os
import sys
from pathlib import Path
from openai import OpenAI

# ── 配置（与 ingest_api.py 保持一致）──
API_KEY  = os.environ.get("DASHSCOPE_API_KEY", "")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL    = "qwen-plus"

WIKI_DIR  = Path(__file__).parent
PAGES_DIR = WIKI_DIR / "pages"

def read_all_pages():
    """读取所有 wiki 页面"""
    pages = {}
    for md in PAGES_DIR.rglob("*.md"):
        rel = str(md.relative_to(WIKI_DIR))
        pages[rel] = md.read_text()
    return pages

def build_query_prompt(question, pages):
    """构建问答 prompt"""
    # 拼接所有页面内容
    wiki_content = ""
    for path, content in sorted(pages.items()):
        wiki_content += f"\n\n=== {path} ===\n{content}"

    return f"""你是一个基于个人 wiki 知识库的问答助手。请根据以下 wiki 内容回答用户的问题。

要求：
- 只根据 wiki 中的内容回答，不要编造
- 如果 wiki 中没有相关信息，明确说明"wiki 中暂无相关内容"
- 引用具体的 wiki 页面名称，用 [[页面名]] 格式
- 回答要有深度，包含具体的数据、公式、对比等细节
- 用中文回答

## Wiki 知识库内容
{wiki_content}

## 用户问题
{question}
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

    pages = read_all_pages()
    print(f"已加载 {len(pages)} 个 wiki 页面\n")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    prompt = build_query_prompt(question, pages)

    print(f"问题：{question}\n")
    print("─" * 50)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.2,
        stream=True,
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n")

if __name__ == "__main__":
    main()
