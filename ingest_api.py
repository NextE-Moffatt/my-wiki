#!/usr/bin/env python3
"""
Wiki Inbox Ingest — 模型无关版本
支持任何 OpenAI 兼容 API：Claude / Qwen / DeepSeek / GPT 等
"""

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import date
from openai import OpenAI


def api_call_with_retry(client, model, messages, max_tokens=8000, temperature=0.3, retries=3):
    """带重试的 API 调用，处理连接超时"""
    # 用更长超时的临时 client
    retry_client = OpenAI(
        api_key=client.api_key,
        base_url=str(client.base_url),
        timeout=300,  # 5 分钟超时
    )
    for attempt in range(retries):
        try:
            response = retry_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < retries - 1:
                wait = 10 * (attempt + 1)
                print(f"    [重试 {attempt+1}/{retries}] {e}，等待 {wait}s...")
                time.sleep(wait)
            else:
                raise e

def extract_pdf_text(pdf_path, max_pages=50):
    """将 PDF 转为文本。支持文本 PDF 和扫描 PDF。

    优先级：
      1. pymupdf4llm（文本 PDF → Markdown，表格保留良好）
      2. pypdf（兜底文本提取）
    对于扫描 PDF，返回 None，由调用方使用视觉 API 处理。
    """
    pdf_path = Path(pdf_path)

    try:
        import pymupdf
        doc = pymupdf.open(str(pdf_path))
        total = min(len(doc), max_pages)

        # 检测是否为扫描 PDF（前 5 页无文字）
        sample_text = ""
        for i in range(min(5, len(doc))):
            sample_text += doc[i].get_text().strip()

        if len(sample_text) > 100:
            # 文本 PDF → pymupdf4llm（保留表格结构）
            try:
                import pymupdf4llm
                md = pymupdf4llm.to_markdown(str(pdf_path), pages=list(range(total)))
                if len(md.strip()) > 100:
                    doc.close()
                    return f"[pymupdf4llm 解析，共 {total}/{len(doc)} 页]\n\n{md}"
            except Exception:
                text = "\n".join(doc[i].get_text() for i in range(total))
                if text.strip():
                    doc.close()
                    return f"[PyMuPDF 文本提取，共 {total}/{len(doc)} 页]\n\n{text.strip()}"
        else:
            # 扫描 PDF → 返回 None，标记需要视觉 API 处理
            doc.close()
            return None

        doc.close()
    except ImportError:
        pass
    except Exception:
        pass

    # pypdf fallback
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages[:max_pages])
        if text.strip():
            return f"[pypdf 解析]\n\n{text.strip()}"
    except ImportError:
        pass
    except Exception:
        pass

    return None  # 无法提取文本


def pdf_to_page_images(pdf_path, start_page=0, end_page=None, dpi=200):
    """将 PDF 页面渲染为 base64 图片列表（供视觉 API 使用）"""
    import base64
    import pymupdf
    doc = pymupdf.open(str(pdf_path))
    if end_page is None:
        end_page = len(doc)
    end_page = min(end_page, len(doc))

    images = []
    mat = pymupdf.Matrix(dpi / 72, dpi / 72)
    for i in range(start_page, end_page):
        pix = doc[i].get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        b64 = base64.b64encode(img_bytes).decode("utf-8")
        images.append({"page": i + 1, "base64": b64})
    doc.close()
    return images


def vision_extract_pages(client, images, batch_label=""):
    """用视觉模型（Qwen-VL）识别 PDF 页面图片，还原文本和表格为 Markdown"""
    VISION_MODEL = "qwen-vl-max"  # 通义千问视觉模型

    content = [
        {"type": "text", "text": (
            "请精确识别以下 PDF 页面图片中的所有内容，转换为 Markdown 格式。\n"
            "要求：\n"
            "1. 表格必须用 Markdown 表格语法还原（| 列1 | 列2 |）\n"
            "2. 公式用 LaTeX 语法（$...$）\n"
            "3. 保留标题层级（#, ##, ###）\n"
            "4. 代码用 ```代码块``` 包裹\n"
            "5. 图片描述用 [图：描述] 标注\n"
            "6. 保持原文内容完整，不要遗漏\n"
            f"以下是 {batch_label} 的页面图片："
        )}
    ]

    for img in images:
        content.append({"type": "text", "text": f"\n--- 第 {img['page']} 页 ---"})
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img['base64']}"}
        })

    import time
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=VISION_MODEL,
                messages=[{"role": "user", "content": content}],
                max_tokens=8000,
                temperature=0.1,
                timeout=120,
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
            else:
                raise e

# ── 配置区 ──────────────────────────────────────────────
# 切换模型只需改这三行

PROVIDER = "qwen"   # 备注用，不影响逻辑

API_KEY  = os.environ.get("DASHSCOPE_API_KEY", "")   # Qwen：export DASHSCOPE_API_KEY=sk-...
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL    = "qwen-plus"

# 其他模型示例（注释掉上面三行，取消注释对应的三行）:
# Claude API:  API_KEY=os.environ.get("ANTHROPIC_API_KEY"), BASE_URL="https://api.anthropic.com/v1", MODEL="claude-sonnet-4-6"
# DeepSeek:    API_KEY=os.environ.get("DEEPSEEK_API_KEY"),  BASE_URL="https://api.deepseek.com/v1",   MODEL="deepseek-chat"
# GPT-4o:      API_KEY=os.environ.get("OPENAI_API_KEY"),    BASE_URL="https://api.openai.com/v1",     MODEL="gpt-4o"
# ────────────────────────────────────────────────────────

WIKI_DIR   = Path(__file__).parent
INBOX_DIR  = WIKI_DIR / "inbox"
PROCESSED  = WIKI_DIR / "inbox_processed"
PAGES_DIR  = WIKI_DIR / "pages"

# 大文件分段阈值（字符数）
CHUNK_SIZE = 6000   # 每段约 6000 字，确保模型能深度理解
CHUNK_OVERLAP = 500 # 段间重叠，避免割裂上下文

def log(msg):
    from datetime import datetime
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {msg}"
    print(line)
    with open(WIKI_DIR / "ingest.log", "a") as f:
        f.write(line + "\n")

def read_inbox_files():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    files = [f for f in INBOX_DIR.iterdir()
             if f.is_file() and f.suffix.lower() in (".md", ".pdf")]
    return files

def read_existing_pages():
    """读取所有现有 wiki 页面，供 AI 参考"""
    pages = {}
    for md in PAGES_DIR.rglob("*.md"):
        rel = md.relative_to(WIKI_DIR)
        pages[str(rel)] = md.read_text()
    return pages

def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """将长文本按段落边界切分为多个 chunk，段间有重叠"""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > chunk_size and current:
            chunks.append(current.strip())
            # 保留重叠：取当前 chunk 末尾的 overlap 字符作为下一段开头
            tail = current[-overlap:] if len(current) > overlap else current
            current = tail + "\n\n" + para
        else:
            current = current + "\n\n" + para if current else para

    if current.strip():
        chunks.append(current.strip())

    return chunks

def read_file_content(f):
    """读取单个 inbox 文件的全部文本"""
    if f.suffix.lower() == ".pdf":
        return extract_pdf_text(f)
    else:
        return f.read_text()

def build_prompt_single(content, filename, existing_pages, chunk_info=None):
    """为单个文档（或单个分段）构建 prompt"""
    schema = (WIKI_DIR / "schema.md").read_text()
    index = (WIKI_DIR / "index.md").read_text()
    pages_summary = "\n".join(f"- {p}" for p in existing_pages.keys())

    chunk_note = ""
    if chunk_info:
        i, total = chunk_info
        chunk_note = f"\n\n> 注意：这是 **{filename}** 的第 {i}/{total} 段。请只根据本段内容生成页面，不要猜测未展示的部分。"

    return f"""你是一个 wiki 管理助手。请深度阅读以下内容，提取关键知识点，摄入到 wiki 知识库。

## Wiki 规则（schema）
{schema}

## 当前 index
{index}

## 现有页面列表
{pages_summary}

## 待摄入的内容：{filename}
{chunk_note}

{content}

## 你的任务

**深度处理要求**：
- 仔细阅读全文，提取每一个有价值的知识点
- 每个 wiki 页面应包含具体的技术细节、数据、公式、结论，而非泛泛的概述
- 如果原文有具体的数字、实验结果、对比数据，务必保留
- 页面之间用 [[wikilink]] 互相链接，形成知识网络

请输出需要创建或更新的 wiki 页面，格式如下：

每个页面用以下分隔符包裹：
<<<FILE: pages/分类/文件名.md>>>
（文件内容）
<<<END>>>

要求：
1. 根据内容丰富度，新建或更新 5-15 个页面（宁精勿滥）
2. 每个页面包含：概述、详细内容（要有深度！）、相关页面（[[链接]]格式）、来源
3. 更新 index.md（也用 <<<FILE: index.md>>> 格式输出）
4. 追加一条 log.md 记录（<<<FILE: log.md>>> 格式，只输出新增的那一段）

今天日期：{date.today()}
"""

def parse_response(response_text):
    """从 AI 输出中解析出文件路径和内容"""
    import re
    pattern = r'<<<FILE:\s*(.+?)>>>\n(.*?)<<<END>>>'
    matches = re.findall(pattern, response_text, re.DOTALL)
    return {path.strip(): content.strip() for path, content in matches}

def write_files(file_map):
    """将解析出的文件写入磁盘"""
    written = []
    for rel_path, content in file_map.items():
        full_path = WIKI_DIR / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # log.md 追加而非覆盖
        if rel_path == "log.md" and full_path.exists():
            existing = full_path.read_text()
            full_path.write_text(content + "\n\n---\n\n" + existing)
        else:
            full_path.write_text(content)
        written.append(rel_path)
    return written

def ingest_text_chunks(client, content, filename, existing_pages):
    """处理文本内容：分段深度处理"""
    chunks = split_into_chunks(content)
    total_written = []

    if len(chunks) == 1:
        log(f"  处理 {filename}（{len(content)} 字，1 段）")
        prompt = build_prompt_single(content, filename, existing_pages)
        result = api_call_with_retry(client, MODEL,
            [{"role": "user", "content": prompt}])
        file_map = parse_response(result)
        if file_map:
            written = write_files(file_map)
            total_written.extend(written)
            log(f"  → 写入 {len(written)} 个文件")
        else:
            log(f"  → 警告：AI 未输出任何文件")
            with open(WIKI_DIR / "ingest.log", "a") as logf:
                logf.write(f"\n--- AI 原始输出 ({filename}) ---\n{result}\n---\n")
    else:
        log(f"  处理 {filename}（{len(content)} 字，分 {len(chunks)} 段）")
        for i, chunk in enumerate(chunks, 1):
            log(f"  段 {i}/{len(chunks)}（{len(chunk)} 字）...")
            prompt = build_prompt_single(
                chunk, filename, existing_pages, chunk_info=(i, len(chunks))
            )
            result = api_call_with_retry(client, MODEL,
                [{"role": "user", "content": prompt}])
            file_map = parse_response(result)
            if file_map:
                written = write_files(file_map)
                total_written.extend(written)
                log(f"    → 写入 {len(written)} 个文件")
                existing_pages = read_existing_pages()
            else:
                log(f"    → 警告：段 {i} AI 未输出任何文件")
                with open(WIKI_DIR / "ingest.log", "a") as logf:
                    logf.write(f"\n--- AI 原始输出 ({filename} 段{i}) ---\n{result}\n---\n")

    return total_written


def ingest_scanned_pdf(client, f, existing_pages, pages_per_batch=4, max_pages=50):
    """处理扫描 PDF：
    第 1 步：视觉模型批量 OCR（只转文字，不做分析）→ 省 token
    第 2 步：合并文本 → 走普通的文本分段 ingest 流程
    """
    import pymupdf
    doc = pymupdf.open(str(f))
    total = min(len(doc), max_pages)
    doc.close()

    # ── 第 1 步：视觉 OCR，只转文字 ──
    num_batches = (total + pages_per_batch - 1) // pages_per_batch
    log(f"  第1步：视觉OCR（{total}页，{num_batches}批）")

    all_text_parts = []
    for batch_idx in range(num_batches):
        start = batch_idx * pages_per_batch
        end = min(start + pages_per_batch, total)
        log(f"    OCR 第{start+1}-{end}页...")

        images = pdf_to_page_images(f, start_page=start, end_page=end, dpi=100)

        try:
            md_text = vision_extract_pages(
                client, images,
                batch_label=f"{f.name} 第{start+1}-{end}页"
            )
            if md_text and len(md_text.strip()) > 20:
                all_text_parts.append(md_text.strip())
                log(f"    → {len(md_text)} 字")
            else:
                log(f"    → 内容太少，跳过")
        except Exception as e:
            log(f"    → OCR 失败：{e}")

    if not all_text_parts:
        log(f"  视觉 OCR 未提取到任何文本")
        return []

    # ── 第 2 步：合并文本，走文本分段 ingest ──
    full_text = f"[视觉OCR解析，{f.name}，共{total}页]\n\n" + "\n\n".join(all_text_parts)
    log(f"  第2步：合并文本（{len(full_text)}字），开始分段 ingest")
    return ingest_text_chunks(client, full_text, f.name, existing_pages)


def ingest_one_file(client, f, existing_pages):
    """处理单个文件：自动选择文本模式或视觉模式"""
    if f.suffix.lower() == ".pdf":
        # 先尝试文本提取
        content = extract_pdf_text(f)
        if content is not None:
            # 文本 PDF → 走文本分段流程
            log(f"  文本 PDF，走文本模式")
            return ingest_text_chunks(client, content, f.name, existing_pages)
        else:
            # 扫描 PDF → 走视觉模式
            log(f"  扫描 PDF，走视觉模式（Qwen-VL）")
            return ingest_scanned_pdf(client, f, existing_pages)
    else:
        # Markdown 文件
        content = f.read_text()
        return ingest_text_chunks(client, content, f.name, existing_pages)

    return total_written

def main():
    files = read_inbox_files()
    if not files:
        log("inbox 为空，跳过")
        return

    log(f"发现 {len(files)} 个文件：{[f.name for f in files]}")

    if not API_KEY:
        log(f"错误：未设置 API Key（当前 PROVIDER={PROVIDER}）")
        sys.exit(1)

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # ── 核心策略：一次一份，深度处理 ──
    for f in files:
        log(f"开始处理：{f.name}")
        existing_pages = read_existing_pages()  # 每份文件前刷新，看到之前生成的页面
        written = ingest_one_file(client, f, existing_pages)

        if written:
            log(f"完成 {f.name}：共写入 {len(written)} 个文件")
        else:
            log(f"警告：{f.name} 未生成任何页面")

        # 移动已处理文件
        shutil.move(str(f), str(PROCESSED / f.name))
        log(f"已移动 {f.name} 到 inbox_processed/")

        # 每处理完一份就 git commit，方便单独回退
        try:
            import subprocess
            subprocess.run(
                ["git", "-C", str(WIKI_DIR), "add", "-A"],
                check=True, capture_output=True
            )
            subprocess.run(
                ["git", "-C", str(WIKI_DIR), "commit",
                 "-m", f"ingest: {f.name}"],
                check=True, capture_output=True
            )
            log(f"已 git commit（可用 'git revert HEAD' 回退此份）")
        except Exception as e:
            log(f"git commit 失败（不影响 wiki 内容）：{e}")

if __name__ == "__main__":
    main()
