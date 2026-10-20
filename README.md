# ⚡ StackPilot & Base of AGI MCP Server

Every time I start building a new Micro-SaaS or AI Agent workflow, I end up opening 30 browser tabs across the same GitHub lists. StackPilot indexes these five openly licensed lists by default:

1. **`punkpeye/awesome-mcp-servers`** (4,382 MCP servers) — MIT
2. **`f/prompts.chat`** (2,512 AI system prompts & developer personas) — CC0 1.0 (prompts) / MIT (code)
3. **`public-apis/public-apis`** (2,185 free REST APIs) — MIT
4. **`awesome-selfhosted/awesome-selfhosted`** (1,263 self-hosted Docker alternatives) — CC BY-SA 3.0
5. **`codecrafters-io/build-your-own-x`** (359 step-by-step architecture tutorials) — CC0 1.0

Item counts are per-source counts from the October 2026 index build.

Searching across raw Markdown files in several repositories takes hours—so I built a parser that normalizes the items into a single **SQLite FTS5 (Full-Text Search + BM25 ranking)** database and wrapped it in a **Model Context Protocol (MCP) Server** + interactive web generator.

Two lists used in earlier versions (`ripienaar/free-for-dev`, `DigitalPlatDev/FreeDomain`) were removed for licensing reasons and are excluded by default. See [LICENSES-AND-ATTRIBUTION.md](LICENSES-AND-ATTRIBUTION.md).

---

## ⚡ Try the Free Interactive $0/Month Stack Generator

👉 **Live Generator:** [https://baseofagi.com/stackpilot](https://baseofagi.com/stackpilot)

Pick any Micro-SaaS niche (AI Coding & MCP Agent, FinTech & Crypto Tracker, SEO & Scraping Automation, DevOps Monitoring, etc.) and it immediately outputs:
- **Free REST APIs** (`Auth`, `HTTPS`, `CORS` flags)
- **Self-Hosted Open-Source Alternatives**
- **Matching MCP Servers**
- **One-Click `.cursorrules` / `CLAUDE.md` / `GEMINI.md` Export**

---

## 🛠️ How the SQLite FTS5 + BM25 Index Works

Instead of using a heavy vector database that requires paid embeddings, SQLite's built-in `fts5` extension with `porter unicode61` tokenization queries the whole index locally:

```sql
CREATE VIRTUAL TABLE resources_fts USING fts5(
    source,
    category,
    title,
    description,
    url UNINDEXED,
    tokenize = 'porter unicode61'
);
```

When an AI coding agent (Claude Code, Cursor, Windsurf, or Antigravity) calls the MCP tool `hub_search(query="email verification", source="public-apis")`, it gets ranked, structured JSON results immediately without hallucinating deprecated APIs or expensive SaaS tools.

`mcp_hub_server.py` drops results from `free-for-dev` and `FreeDomain` by default, even if an older index still contains them. The `STACKPILOT_EXCLUDE_SOURCES` environment variable (comma-separated source names) replaces that default list; only change it for an index you built yourself from lists whose licenses you have checked.

This repository contains the MCP server code only. It does not include the `search_hub` module or an index database (`hub.db`), which the server needs to run.

---

## 📦 StackPilot Pro

StackPilot Pro (offline database + MCP server + 50 SaaS blueprints) is **temporarily unavailable** while its licensing is being corrected.

- **Interactive Web Builder:** [https://baseofagi.com/stackpilot](https://baseofagi.com/stackpilot)

---

## Sources & licenses

Each indexed list keeps its own license. Full source and license table: [LICENSES-AND-ATTRIBUTION.md](LICENSES-AND-ATTRIBUTION.md).
