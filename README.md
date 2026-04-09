# my-wiki

A personal AI/tech research knowledge base, built with Markdown and Obsidian, maintained by Claude Code.

## What This Is

A structured wiki for accumulating notes on AI research papers, concepts, people, and trends. Content is ingested from articles, papers, and web clips, then organized into interlinked pages automatically.

## Structure

```
my_wiki/
├── pages/
│   ├── concepts/     # Core concepts (attention, scaling, etc.)
│   ├── models/       # Specific models (GPT, LLaMA, etc.)
│   ├── papers/       # Paper summaries
│   ├── people/       # Researchers and institutions
│   ├── trends/       # Industry trends and timelines
│   └── tools/        # Frameworks and libraries
├── inbox/            # Raw clippings, pending ingestion
├── index.md          # Full page directory
├── log.md            # Ingestion history
└── schema.md         # Page format rules
```

## Current Pages

**Papers**
- [The Bitter Lesson](pages/papers/bitter_lesson.md) — Rich Sutton, 2019
- [Attention Is All You Need](pages/papers/attention_is_all_you_need.md) — Vaswani et al., 2017

**Concepts**
- [Scaling Computation](pages/concepts/scaling_computation.md)
- [Search and Learning](pages/concepts/search_and_learning.md)
- [Attention Mechanism](pages/concepts/attention_mechanism.md)

**People**
- [Rich Sutton](pages/people/rich_sutton.md)

**Trends**
- [Human Knowledge vs Computation](pages/trends/human_knowledge_vs_computation.md)

## How It Works

**Reading**: Open this folder as an [Obsidian](https://obsidian.md) vault. All `[[wikilinks]]` resolve automatically, and Graph View shows the knowledge network.

**Adding content**: Drop a clipping into `inbox/` via [Obsidian Web Clipper](https://obsidian.md/clipper), or paste a URL/article into Claude Code with `"add this to my wiki"`. Claude reads the content, creates or updates relevant pages, maintains cross-links, and updates `index.md` and `log.md`.

**Page format**: Every page follows the schema in `schema.md` — overview, detail, related pages (`[[links]]`), and sources.

## Automated Ingestion

`ingest.sh` checks `inbox/` for new files and calls the Claude CLI to process them. It runs daily via launchd and also triggers on file changes.

For model-agnostic ingestion (Qwen, DeepSeek, GPT, etc.), use `ingest_api.py`:

```bash
# Configure in ingest_api.py: BASE_URL, MODEL, API_KEY env var
export DASHSCOPE_API_KEY=sk-...
python3 ingest_api.py
```
