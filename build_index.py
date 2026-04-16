#!/usr/bin/env python3
"""
构建双层检索索引：
  1. Wiki 页面索引（AI 提炼过的结构化知识）
  2. 原始文档切片索引（保留细节的原文 chunks）

使用 DashScope text-embedding-v3 计算向量。
用法：DASHSCOPE_API_KEY=sk-... python3 build_index.py
"""

import os
import sys
import json
import time
from pathlib import Path
from openai import OpenAI

# ── 配置 ──
API_KEY  = os.environ.get("DASHSCOPE_API_KEY", "")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
EMBED_MODEL = "text-embedding-v3"
EMBED_DIM = 1024  # text-embedding-v3 默认维度

WIKI_DIR     = Path(__file__).parent
PAGES_DIR    = WIKI_DIR / "pages"
PROCESSED    = WIKI_DIR / "inbox_processed"
INDEX_DIR    = WIKI_DIR / "index"
CHUNK_SIZE   = 800   # 原始文档切片大小（字符）
CHUNK_OVERLAP = 100  # 切片重叠


def get_embeddings(client, texts, batch_size=6):
    """批量计算 embedding，返回向量列表"""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        # 截断过长文本（API 限制）
        batch = [t[:8000] for t in batch]
        for attempt in range(3):
            try:
                response = client.embeddings.create(
                    model=EMBED_MODEL,
                    input=batch,
                    dimensions=EMBED_DIM,
                )
                all_embeddings.extend([d.embedding for d in response.data])
                break
            except Exception as e:
                if attempt < 2:
                    print(f"  [重试] {e}")
                    time.sleep(5)
                else:
                    raise
        if i + batch_size < len(texts):
            time.sleep(0.5)  # 避免 rate limit
    return all_embeddings


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """将文本按段落边界切分为 chunks"""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > chunk_size and current:
            chunks.append(current.strip())
            tail = current[-overlap:] if len(current) > overlap else current
            current = tail + "\n\n" + para
        else:
            current = current + "\n\n" + para if current else para

    if current.strip():
        chunks.append(current.strip())

    return chunks


def extract_text_from_file(f):
    """从文件提取文本"""
    if f.suffix.lower() == ".pdf":
        # 用 ingest_api 的 PDF 提取（优先 pymupdf4llm，OCR 兜底）
        try:
            sys.path.insert(0, str(WIKI_DIR))
            from ingest_api import extract_pdf_text, pdf_to_page_images, vision_extract_pages
            text = extract_pdf_text(f, max_pages=100)
            if text:
                return text

            # 扫描 PDF → 视觉 OCR
            print(f"  扫描 PDF，使用视觉 OCR...")
            client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
            import pymupdf
            doc = pymupdf.open(str(f))
            total = min(len(doc), 100)
            doc.close()

            parts = []
            for start in range(0, total, 2):
                end = min(start + 2, total)
                images = pdf_to_page_images(f, start_page=start, end_page=end, dpi=100)
                try:
                    md = vision_extract_pages(client, images, batch_label=f"{f.name} p{start+1}-{end}")
                    if md and len(md.strip()) > 20:
                        parts.append(md.strip())
                        print(f"    p{start+1}-{end}: {len(md)} 字")
                except Exception as e:
                    print(f"    p{start+1}-{end}: OCR 失败 ({e})")
            return "\n\n".join(parts) if parts else None
        except Exception as e:
            print(f"  PDF 提取失败：{e}")
            return None
    elif f.suffix.lower() in (".md", ".txt"):
        return f.read_text()
    return None


def build_wiki_index(client):
    """构建 wiki 页面索引"""
    print("=== 构建 Wiki 页面索引 ===")
    entries = []
    texts = []

    for md in sorted(PAGES_DIR.rglob("*.md")):
        rel = str(md.relative_to(WIKI_DIR))
        content = md.read_text()
        if len(content.strip()) < 20:
            continue
        # 用标题+概述作为检索文本（更精练）
        entries.append({
            "path": rel,
            "type": "wiki",
            "content": content,
        })
        # embedding 文本 = 文件名 + 内容前 2000 字
        filename = md.stem.replace("_", " ")
        texts.append(f"{filename}\n\n{content[:2000]}")

    print(f"  共 {len(entries)} 个 wiki 页面")
    embeddings = get_embeddings(client, texts)

    for i, entry in enumerate(entries):
        entry["embedding"] = embeddings[i]

    return entries


def build_chunks_index(client):
    """构建原始文档切片索引

    数据来源（按优先级）：
      1. index/raw/ — ingest 时自动保存的提取文本（推荐）
      2. inbox_processed/ 中的 .md 文件
    PDF 不在此处实时 OCR（太慢），应在 ingest 时通过 save_raw_text() 保存。
    """
    print("\n=== 构建原始文档切片索引 ===")
    entries = []
    texts = []

    # 收集所有原始文本来源
    source_files = []

    # 优先从 index/raw/ 读取
    raw_dir = WIKI_DIR / "index" / "raw"
    if raw_dir.exists():
        for f in sorted(raw_dir.iterdir()):
            if f.suffix.lower() in (".md", ".txt") and not f.name.startswith("."):
                source_files.append(f)

    # 补充 inbox_processed/ 中的 md（去重）
    if PROCESSED.exists():
        raw_names = {f.stem for f in source_files}
        for f in sorted(PROCESSED.iterdir()):
            if f.suffix.lower() in (".md", ".txt") and not f.name.startswith("."):
                if f.stem not in raw_names:
                    source_files.append(f)

    if not source_files:
        print("  无原始文档可索引")
        print("  提示：运行 ingest 处理文档后会自动保存原始文本到 index/raw/")
        return entries

    for f in source_files:
        print(f"  处理 {f.name}...")
        text = f.read_text()
        if len(text.strip()) < 50:
            print(f"    跳过（内容太少）")
            continue

        chunks = chunk_text(text)
        print(f"    → {len(chunks)} 个切片")

        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 30:
                continue
            entries.append({
                "source": f.name,
                "chunk_id": i,
                "total_chunks": len(chunks),
                "type": "original",
                "content": chunk.strip(),
            })
            texts.append(chunk.strip()[:8000])

    if texts:
        print(f"  共 {len(entries)} 个切片，计算 embedding...")
        embeddings = get_embeddings(client, texts)
        for i, entry in enumerate(entries):
            entry["embedding"] = embeddings[i]

    return entries


def save_index(wiki_entries, chunk_entries):
    """保存索引到磁盘"""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # 分离 embedding 和 metadata（JSON 更紧凑）
    wiki_index = []
    for e in wiki_entries:
        wiki_index.append({
            "path": e["path"],
            "type": e["type"],
            "content": e["content"],
            "embedding": e["embedding"],
        })

    chunks_index = []
    for e in chunk_entries:
        chunks_index.append({
            "source": e["source"],
            "chunk_id": e["chunk_id"],
            "total_chunks": e["total_chunks"],
            "type": e["type"],
            "content": e["content"],
            "embedding": e["embedding"],
        })

    with open(INDEX_DIR / "wiki_index.json", "w") as f:
        json.dump(wiki_index, f, ensure_ascii=False)
    with open(INDEX_DIR / "chunks_index.json", "w") as f:
        json.dump(chunks_index, f, ensure_ascii=False)

    print(f"\n索引已保存到 {INDEX_DIR}/")
    print(f"  wiki_index.json:   {len(wiki_index)} 条")
    print(f"  chunks_index.json: {len(chunks_index)} 条")


def main():
    if not API_KEY:
        print("错误：请设置 DASHSCOPE_API_KEY 环境变量")
        sys.exit(1)

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    wiki_entries = build_wiki_index(client)
    chunk_entries = build_chunks_index(client)
    save_index(wiki_entries, chunk_entries)
    print("\n✅ 索引构建完成")


if __name__ == "__main__":
    main()
