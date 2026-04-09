#!/bin/bash
# Wiki Inbox Ingest Script
# 检查 inbox/ 是否有待处理文件，有则调用 Claude CLI 摄入

WIKI_DIR="$(cd "$(dirname "$0")" && pwd)"
INBOX="$WIKI_DIR/inbox"
PROCESSED="$WIKI_DIR/inbox/processed"

mkdir -p "$PROCESSED"

# 找出所有待处理的 .md 文件（排除 processed 子目录）
FILES=$(find "$INBOX" -maxdepth 1 -name "*.md" -type f 2>/dev/null)

if [ -z "$FILES" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M')] inbox 为空，跳过"
  exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M')] 发现新文件，开始 ingest..."

# 构建文件列表描述
FILE_LIST=""
for f in $FILES; do
  FILE_LIST="$FILE_LIST\n- $(basename $f)"
done

# 调用后端（默认 Claude CLI；改为 api 则用 ingest_api.py）
BACKEND="${WIKI_BACKEND:-claude}"

if [ "$BACKEND" = "api" ]; then
  python3 "$WIKI_DIR/ingest_api.py"
else
  /Users/xujing/.local/bin/claude --print \
    --allowedTools "Read,Write,Edit,Glob,Grep" \
    --model claude-sonnet-4-6 \
    -p "你是我的 wiki 管理助手。wiki 位于 $WIKI_DIR。

inbox 目录里有以下新文件需要摄入：$FILE_LIST

请：
1. 读取每个 inbox 文件的内容
2. 根据 schema.md 的规则，在 pages/ 下新建或更新相关 wiki 页面
3. 维护交叉链接（[[页面名]] 格式）
4. 更新 index.md 和 log.md
5. 把处理完的文件移动到 inbox/processed/ 目录

开始处理。"
fi

echo "[$(date '+%Y-%m-%d %H:%M')] ingest 完成"
