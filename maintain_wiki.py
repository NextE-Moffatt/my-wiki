#!/usr/bin/env python3
"""
Wiki 定期维护 — 自动检测和修复知识库问题
用法：DASHSCOPE_API_KEY=sk-... python3 maintain_wiki.py [--fix]

检查项：
  1. 死链接：[[wikilink]] 指向不存在的页面
  2. 孤岛页面：没有被任何其他页面引用的页面
  3. 重复页面：标题或内容高度相似的页面
  4. 低质量页面：内容过短或缺少关键结构
  5. 索引同步：检查 embedding 索引是否需要更新

加 --fix 参数时，会调用 AI 自动修复可修复的问题。
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from datetime import date
from collections import defaultdict

WIKI_DIR  = Path(__file__).parent
PAGES_DIR = WIKI_DIR / "pages"
INDEX_DIR = WIKI_DIR / "index"

API_KEY  = os.environ.get("DASHSCOPE_API_KEY", "")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL    = "qwen-plus"


def read_all_pages():
    pages = {}
    for md in PAGES_DIR.rglob("*.md"):
        rel = str(md.relative_to(WIKI_DIR))
        pages[rel] = md.read_text()
    return pages


def extract_wikilinks(content):
    """提取 [[wikilink]] 引用"""
    return re.findall(r'\[\[([^\]]+)\]\]', content)


def check_dead_links(pages):
    """检查死链接"""
    # 构建所有合法目标（文件名不含扩展名，支持多种引用格式）
    valid_targets = set()
    for path in pages:
        # pages/concepts/bpe.md → bpe, concepts/bpe, pages/concepts/bpe
        p = Path(path)
        valid_targets.add(p.stem)                           # bpe
        valid_targets.add(str(p.with_suffix("")))           # pages/concepts/bpe
        valid_targets.add(str(p.parent / p.stem))           # pages/concepts/bpe
        # 也加不含 pages/ 前缀的
        rel = str(p.relative_to("pages")) if str(p).startswith("pages/") else str(p)
        valid_targets.add(str(Path(rel).with_suffix("")))   # concepts/bpe

    dead_links = []
    for path, content in pages.items():
        links = extract_wikilinks(content)
        for link in links:
            # 清理链接
            clean = link.replace(".md", "").strip()
            if clean not in valid_targets:
                dead_links.append((path, link))

    return dead_links


def check_orphan_pages(pages):
    """检查孤岛页面（没有被任何其他页面引用）"""
    # 收集所有被引用的页面
    referenced = set()
    for path, content in pages.items():
        links = extract_wikilinks(content)
        for link in links:
            clean = link.replace(".md", "").strip()
            referenced.add(clean)
            # 也加上可能的变体
            referenced.add(Path(clean).stem)

    orphans = []
    for path in pages:
        p = Path(path)
        stem = p.stem
        rel_no_ext = str(p.with_suffix(""))

        # 检查是否被引用（任何格式）
        is_referenced = (
            stem in referenced or
            rel_no_ext in referenced or
            str(Path(path).relative_to("pages")).replace(".md", "") in referenced
            if str(path).startswith("pages/") else
            stem in referenced or rel_no_ext in referenced
        )

        # index.md 和 schema.md 是特殊页面，不算孤岛
        if not is_referenced and stem not in ("index", "schema", "log"):
            orphans.append(path)

    return orphans


def check_low_quality(pages):
    """检查低质量页面"""
    issues = []
    for path, content in pages.items():
        if Path(path).stem in ("index", "schema", "log"):
            continue

        problems = []
        lines = content.strip().split("\n")

        # 内容过短
        if len(content.strip()) < 100:
            problems.append("内容过短（<100字）")

        # 缺少标题
        if not any(line.startswith("# ") for line in lines):
            problems.append("缺少一级标题")

        # 缺少相关页面
        if "[[" not in content:
            problems.append("无 wikilink 关联")

        # 缺少来源
        if "来源" not in content and "source" not in content.lower():
            problems.append("缺少来源标注")

        if problems:
            issues.append((path, problems))

    return issues


def check_duplicates(pages):
    """检查可能重复的页面（标题相似）"""
    from collections import Counter

    stems = []
    for path in pages:
        stem = Path(path).stem.lower().replace("_", " ").replace("-", " ")
        stems.append((stem, path))

    # 简单的相似度检测：共享大量关键词
    duplicates = []
    seen = set()
    for i, (stem_a, path_a) in enumerate(stems):
        words_a = set(stem_a.split())
        for j, (stem_b, path_b) in enumerate(stems):
            if i >= j:
                continue
            words_b = set(stem_b.split())
            # 如果两个文件名的词集交集占比超过 60%
            if words_a and words_b:
                overlap = len(words_a & words_b)
                min_len = min(len(words_a), len(words_b))
                if min_len > 0 and overlap / min_len >= 0.6 and overlap >= 2:
                    pair = tuple(sorted([path_a, path_b]))
                    if pair not in seen:
                        seen.add(pair)
                        duplicates.append(pair)

    return duplicates


def check_index_sync(pages):
    """检查索引是否需要更新"""
    wiki_index_path = INDEX_DIR / "wiki_index.json"
    if not wiki_index_path.exists():
        return "未建立", len(pages)

    import json
    with open(wiki_index_path) as f:
        index = json.load(f)
    indexed_paths = {e["path"] for e in index}
    current_paths = set(pages.keys())

    missing = current_paths - indexed_paths
    stale = indexed_paths - current_paths
    return len(missing), len(stale)


def fix_dead_links(pages, dead_links):
    """尝试修复死链接"""
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # 按源文件分组
    by_source = defaultdict(list)
    for source, link in dead_links:
        by_source[source].append(link)

    existing_pages = "\n".join(f"- {p}" for p in sorted(pages.keys()))
    fixed_count = 0

    for source, links in by_source.items():
        links_str = ", ".join(f"[[{l}]]" for l in links)
        prompt = f"""以下 wiki 页面中有死链接需要修复：

文件：{source}
死链接：{links_str}

现有的所有页面：
{existing_pages}

请为每个死链接找到最合适的现有页面替换。如果找不到合适的，建议删除该链接。

输出格式（每行一个）：
[[原链接]] → [[新链接]]
或
[[原链接]] → 删除
"""
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.1,
        )

        result = response.choices[0].message.content
        content = pages[source]
        full_path = WIKI_DIR / source

        for line in result.strip().split("\n"):
            if "→" in line and "删除" in line:
                # 删除链接
                match = re.search(r'\[\[(.+?)\]\]', line)
                if match:
                    old_link = match.group(1)
                    # 把 [[link]] 替换为纯文本
                    content = content.replace(f"[[{old_link}]]", old_link)
                    fixed_count += 1
            elif "→" in line:
                parts = line.split("→")
                if len(parts) == 2:
                    old_match = re.search(r'\[\[(.+?)\]\]', parts[0])
                    new_match = re.search(r'\[\[(.+?)\]\]', parts[1])
                    if old_match and new_match:
                        content = content.replace(
                            f"[[{old_match.group(1)}]]",
                            f"[[{new_match.group(1)}]]"
                        )
                        fixed_count += 1

        full_path.write_text(content)

    return fixed_count


def main():
    auto_fix = "--fix" in sys.argv

    pages = read_all_pages()
    print(f"📊 Wiki 维护报告 — {date.today()}")
    print(f"   共 {len(pages)} 个页面\n")

    all_ok = True

    # 1. 死链接
    dead_links = check_dead_links(pages)
    if dead_links:
        all_ok = False
        print(f"❌ 死链接：{len(dead_links)} 个")
        for source, link in dead_links[:10]:
            print(f"   {source} → [[{link}]]")
        if len(dead_links) > 10:
            print(f"   ... 还有 {len(dead_links) - 10} 个")
        if auto_fix and API_KEY:
            print(f"\n   🔧 自动修复死链接...")
            fixed = fix_dead_links(pages, dead_links)
            print(f"   ✅ 修复了 {fixed} 个")
    else:
        print("✅ 无死链接")

    # 2. 孤岛页面
    orphans = check_orphan_pages(pages)
    if orphans:
        all_ok = False
        print(f"\n⚠️  孤岛页面（未被引用）：{len(orphans)} 个")
        for o in orphans[:10]:
            print(f"   {o}")
        if len(orphans) > 10:
            print(f"   ... 还有 {len(orphans) - 10} 个")
    else:
        print("\n✅ 无孤岛页面")

    # 3. 可能重复
    duplicates = check_duplicates(pages)
    if duplicates:
        all_ok = False
        print(f"\n⚠️  可能重复的页面：{len(duplicates)} 对")
        for a, b in duplicates[:5]:
            print(f"   {a}  ↔  {b}")
    else:
        print("\n✅ 无疑似重复页面")

    # 4. 低质量页面
    low_quality = check_low_quality(pages)
    if low_quality:
        all_ok = False
        print(f"\n⚠️  低质量页面：{len(low_quality)} 个")
        for path, problems in low_quality[:10]:
            print(f"   {path}：{', '.join(problems)}")
        if len(low_quality) > 10:
            print(f"   ... 还有 {len(low_quality) - 10} 个")
    else:
        print("\n✅ 所有页面质量达标")

    # 5. 索引同步
    result = check_index_sync(pages)
    if result == ("未建立", len(pages)):
        print(f"\n⚠️  索引未建立（运行 wiki-index 构建）")
    else:
        missing, stale = result
        if missing > 0 or stale > 0:
            all_ok = False
            print(f"\n⚠️  索引不同步：{missing} 个新页面未索引，{stale} 个已删除页面残留")
            print(f"   运行 wiki-index 更新")
        else:
            print("\n✅ 索引已同步")

    # 总结
    print(f"\n{'─' * 50}")
    if all_ok:
        print("🎉 Wiki 状态良好，无需维护")
    else:
        print("📋 建议操作：")
        if dead_links and not auto_fix:
            print("   - 运行 python3 maintain_wiki.py --fix 自动修复死链接")
        if orphans:
            print("   - 检查孤岛页面，考虑添加引用或合并")
        if duplicates:
            print("   - 检查重复页面，合并内容")
        if isinstance(result, tuple) and result[0] != "未建立":
            missing, stale = result
            if missing > 0:
                print("   - 运行 wiki-index 更新索引")

    # 自动 commit 修复
    if auto_fix:
        try:
            subprocess.run(["git", "-C", str(WIKI_DIR), "add", "-A"],
                           check=True, capture_output=True)
            subprocess.run(["git", "-C", str(WIKI_DIR), "commit",
                            "-m", f"maintain: auto-fix {date.today()}"],
                           check=True, capture_output=True)
            print("\n📌 修复已 git commit")
        except Exception:
            pass


if __name__ == "__main__":
    main()
