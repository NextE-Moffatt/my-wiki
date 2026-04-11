#!/usr/bin/env python3
"""
Wiki Inbox Ingest — 模型无关版本
支持任何 OpenAI 兼容 API：Claude / Qwen / DeepSeek / GPT 等
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import date
from openai import OpenAI

def extract_pdf_text(pdf_path):
    """提取 PDF 文字，返回字符串"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text.strip()
    except ImportError:
        return f"[PDF 解析失败：请运行 pip3 install pypdf]"
    except Exception as e:
        return f"[PDF 解析出错：{e}]"

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
SCHEMA     = (WIKI_DIR / "schema.md").read_text()
INDEX      = (WIKI_DIR / "index.md").read_text()

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

def build_prompt(inbox_files, existing_pages):
    inbox_contents = ""
    for f in inbox_files:
        if f.suffix.lower() == ".pdf":
            content = extract_pdf_text(f)
            inbox_contents += f"\n\n=== {f.name} (PDF) ===\n{content}"
        else:
            inbox_contents += f"\n\n=== {f.name} ===\n{f.read_text()}"

    pages_summary = "\n".join(f"- {p}" for p in existing_pages.keys())

    return f"""你是一个 wiki 管理助手。请将 inbox 中的内容摄入到 wiki 知识库。

## Wiki 规则（schema）
{SCHEMA}

## 当前 index
{INDEX}

## 现有页面列表
{pages_summary}

## 待摄入的 inbox 内容
{inbox_contents}

## 你的任务

请输出需要创建或更新的 wiki 页面，格式如下：

每个页面用以下分隔符包裹：
<<<FILE: pages/分类/文件名.md>>>
（文件内容）
<<<END>>>

要求：
1. 新建或更新 10-15 个相关页面
2. 每个页面包含：概述、详细内容、相关页面（[[链接]]格式）、来源
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
    existing_pages = read_existing_pages()
    prompt = build_prompt(files, existing_pages)

    log(f"调用 {MODEL} 处理中...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=8000,
        temperature=0.3,
    )

    result = response.choices[0].message.content
    file_map = parse_response(result)

    if not file_map:
        log("警告：AI 未输出任何文件，请检查 ingest.log")
        with open(WIKI_DIR / "ingest.log", "a") as f:
            f.write("\n--- AI 原始输出 ---\n" + result + "\n---\n")
        sys.exit(1)

    written = write_files(file_map)
    log(f"写入 {len(written)} 个文件：{written}")

    # 移动已处理文件
    for f in files:
        shutil.move(str(f), str(PROCESSED / f.name))
    log(f"已移动到 inbox_processed/")

    # 自动 git commit，方便回退
    try:
        import subprocess
        file_names = ", ".join(f.name for f in files)
        subprocess.run(
            ["git", "-C", str(WIKI_DIR), "add", "-A"],
            check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", str(WIKI_DIR), "commit",
             "-m", f"ingest: {file_names}"],
            check=True, capture_output=True
        )
        log("已自动 git commit（可用 'git revert HEAD' 回退）")
    except Exception as e:
        log(f"git commit 失败（不影响 wiki 内容）：{e}")

if __name__ == "__main__":
    main()
