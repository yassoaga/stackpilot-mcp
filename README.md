# ⚡ StackPilot & Base of AGI MCP Server (12,131 Indexed Developer Resources)

Every time I start building a new Micro-SaaS or AI Agent workflow, I end up opening 30 browser tabs across the same 7 legendary GitHub repositories:

1. **`punkpeye/awesome-mcp-servers`** (4,382 MCP servers)
2. **`f/prompts.chat`** (2,512 AI system prompts & developer personas)
3. **`public-apis/public-apis`** (2,185 free REST APIs)
4. **`ripienaar/free-for-dev`** (1,354 SaaS/PaaS/Cloud free tiers)
5. **`awesome-selfhosted/awesome-selfhosted`** (1,263 self-hosted Docker alternatives)
6. **`codecrafters-io/build-your-own-x`** (359 step-by-step architecture tutorials)
7. **`DigitalPlatDev/FreeDomain`** (76 free domain & DNS guides)

Searching across raw Markdown files in 7 different repositories takes hours—so I built a parser that normalizes all **12,131 items** into a single **SQLite FTS5 (Full-Text Search + BM25 ranking)** database and wrapped it in a **Model Context Protocol (MCP) Server** + interactive web generator.

---

## ⚡ Try the Free Interactive $0/Month Stack Generator

👉 **Live Generator:** [https://baseofagi.com/stackpilot](https://baseofagi.com/stackpilot)

Pick any Micro-SaaS niche (AI Coding & MCP Agent, FinTech & Crypto Tracker, SEO & Scraping Automation, DevOps Monitoring, etc.) and it immediately outputs:
- Verified **Free REST APIs** (`Auth`, `HTTPS`, `CORS` flags)
- **Always-Free Cloud & Database Tiers** (`$0/mo` infrastructure)
- **Self-Hosted Open-Source Alternatives**
- **Matching MCP Servers**
- **One-Click `.cursorrules` / `CLAUDE.md` / `GEMINI.md` Export**

---

## 🛠️ How the SQLite FTS5 + BM25 Index Works

Instead of using a heavy vector database that requires paid embeddings, SQLite's built-in `fts5` extension with `porter unicode61` tokenization queries all 12,131 items in **under 2 milliseconds**:

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

When an AI coding agent (Claude Code, Cursor, Windsurf, or Antigravity) calls the MCP tool `hub_search(query="email verification", source="free-for-dev")`, it gets ranked, structured JSON results immediately without hallucinating deprecated APIs or expensive SaaS tools.

---

## 📦 Want the Full Offline SQLite FTS5 Database + MCP Server + 50 SaaS Blueprints?

If you want to run the entire 12,131-item index locally inside your IDE via MCP—plus get **50 complete Micro-SaaS Architecture Blueprints** (Markdown + JSON) and the **Zero-Cost Cloud Playbook**:

- **StackPilot Pro ($19 One-Time Download):** [https://buy.polar.sh/polar_cl_3xIC5J1D1QAYFVAi7cSSt10ksKVOqQHMsaJCT2uuGwv](https://buy.polar.sh/polar_cl_3xIC5J1D1QAYFVAi7cSSt10ksKVOqQHMsaJCT2uuGwv)
- **Interactive Web Builder:** [https://baseofagi.com/stackpilot](https://baseofagi.com/stackpilot)