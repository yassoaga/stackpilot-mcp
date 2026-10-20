import json
import os
import sys
from pathlib import Path

# Add project directory to sys.path so search_hub can be imported from anywhere
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from search_hub import get_stats, search_items

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")


# Sources left out by default for licensing reasons (see LICENSES-AND-ATTRIBUTION.md):
#   free-for-dev (ripienaar/free-for-dev): no license file -> all rights reserved
#   FreeDomain (DigitalPlatDev/FreeDomain): GNU AGPL-3.0
# Results from these sources are dropped even if an older index still contains them.
# STACKPILOT_EXCLUDE_SOURCES (comma-separated source names) replaces this list; only
# change it for an index you built yourself from lists whose licenses you have checked.
DEFAULT_EXCLUDED_SOURCES = ("free-for-dev", "FreeDomain")


def excluded_sources() -> list:
    raw = os.environ.get("STACKPILOT_EXCLUDE_SOURCES")
    names = DEFAULT_EXCLUDED_SOURCES if raw is None else raw.split(",")
    return [n.strip() for n in names if n.strip()]


def is_excluded(source, excluded: list) -> bool:
    return str(source or "").strip().lower() in {n.lower() for n in excluded}


def filtered_search(query: str, source: str = "", category: str = "", limit: int = 15) -> dict:
    excluded = excluded_sources()

    if source and source != "all":
        if is_excluded(source, excluded):
            return {
                "total": 0,
                "count": 0,
                "results": [],
                "note": f"Source '{source}' is excluded by default for licensing reasons (see LICENSES-AND-ATTRIBUTION.md)."
            }
        return search_items(query=query, source=source, category=category, limit=limit)

    if not excluded:
        return search_items(query=query, source="", category=category, limit=limit)

    # No source filter: skip rows from excluded sources and page until `limit` rows are collected.
    total_all = search_items(query=query, source="", category=category, limit=0)["total"]
    excluded_total = sum(
        search_items(query=query, source=name, category=category, limit=0)["total"] for name in excluded
    )

    results = []
    offset = 0
    page = max(limit * 2, 50)
    while len(results) < limit and offset < total_all:
        batch = search_items(query=query, source="", category=category, limit=page, offset=offset)["results"]
        if not batch:
            break
        results.extend(r for r in batch if not is_excluded(r.get("source"), excluded))
        offset += page

    results = results[:limit]
    return {"total": max(total_all - excluded_total, 0), "count": len(results), "results": results}


def filtered_stats() -> dict:
    stats = get_stats()
    excluded = excluded_sources()
    if not isinstance(stats, dict) or not isinstance(stats.get("sources"), dict):
        return stats

    sources = {name: info for name, info in stats["sources"].items() if not is_excluded(name, excluded)}
    out = dict(stats)
    out["sources"] = sources
    out["total"] = sum(int(info.get("count", 0)) for info in sources.values() if isinstance(info, dict))
    out["excluded_sources"] = excluded
    return out


TOOLS = [
    {
        "name": "hub_search",
        "description": "Search across the indexed developer resource lists (build-your-own-x, public-apis, awesome-mcp-servers, prompts.chat, awesome-selfhosted).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keywords (e.g., 'weather api', 'database', 'docker', 'authentication')"},
                "source": {
                    "type": "string",
                    "description": "Optional filter: 'build-your-own-x', 'public-apis', 'awesome-mcp-servers', 'prompts.chat', or 'awesome-selfhosted'"
                },
                "category": {"type": "string", "description": "Optional category filter"},
                "limit": {"type": "integer", "description": "Max items to return (default 15)", "default": 15}
            },
            "required": ["query"]
        }
    },
    {
        "name": "hub_find_public_api",
        "description": "Find free public APIs from public-apis (2,185+ APIs) by topic, category, or auth requirement.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "API topic or keyword (e.g., 'crypto', 'weather', 'geocoding', 'music')"},
                "category": {"type": "string", "description": "Optional category name (e.g., 'Weather', 'Finance', 'Animals', 'Anime')"},
                "limit": {"type": "integer", "default": 15}
            },
            "required": ["query"]
        }
    },
    {
        "name": "hub_find_prompt",
        "description": "Search 2,500+ curated system prompts and personas from prompts.chat (Awesome ChatGPT Prompts).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Role or task keyword (e.g., 'Linux', 'React', 'Security', 'SQL', 'Architect')"},
                "devs_only": {"type": "boolean", "description": "Filter only developer-focused prompts", "default": False},
                "limit": {"type": "integer", "default": 10}
            },
            "required": ["query"]
        }
    },
    {
        "name": "hub_find_selfhosted",
        "description": "Search 1,260+ open-source self-hosted software packages from awesome-selfhosted.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Software type, feature, or stack (e.g., 'analytics', 'crm', 'docker', 'wiki', 'vpn')"},
                "category": {"type": "string", "description": "Optional category filter"},
                "limit": {"type": "integer", "default": 15}
            },
            "required": ["query"]
        }
    },
    {
        "name": "hub_find_mcp_server",
        "description": "Search 4,380+ Model Context Protocol (MCP) servers from awesome-mcp-servers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Capability or integration keyword (e.g., 'postgres', 'browser', 'github', 'slack', 'docker')"},
                "category": {"type": "string", "description": "Optional category filter (e.g., 'Databases', 'Browser Automation', 'Developer Tools')"},
                "limit": {"type": "integer", "default": 15}
            },
            "required": ["query"]
        }
    },
    {
        "name": "hub_find_tutorial",
        "description": "Search 350+ step-by-step 'Build Your Own X' guides (Docker, Git, DB, LLM, Compiler, OS, etc.) from codecrafters-io/build-your-own-x.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Technology or language (e.g., 'database python', 'docker', 'git', 'neural network', 'rust')"},
                "limit": {"type": "integer", "default": 15}
            },
            "required": ["query"]
        }
    },
    {
        "name": "hub_stats",
        "description": "Get counts and category lists for the indexed repositories in the Developer Resource Hub (sources excluded for licensing reasons are left out).",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def handle_tool_call(name: str, args: dict) -> dict:
    limit = int(args.get("limit", 15))
    query = str(args.get("query", ""))
    category = str(args.get("category", ""))

    if name == "hub_stats":
        data = filtered_stats()
    elif name == "hub_search":
        source = str(args.get("source", ""))
        data = filtered_search(query=query, source=source, category=category, limit=limit)
    elif name == "hub_find_public_api":
        data = filtered_search(query=query, source="public-apis", category=category, limit=limit)
    elif name == "hub_find_prompt":
        cat = "Developer Prompts" if args.get("devs_only") else category
        data = filtered_search(query=query, source="prompts.chat", category=cat, limit=limit)
    elif name == "hub_find_selfhosted":
        data = filtered_search(query=query, source="awesome-selfhosted", category=category, limit=limit)
    elif name == "hub_find_mcp_server":
        data = filtered_search(query=query, source="awesome-mcp-servers", category=category, limit=limit)
    elif name == "hub_find_tutorial":
        data = filtered_search(query=query, source="build-your-own-x", category=category, limit=limit)
    else:
        return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(data, indent=2, ensure_ascii=False)
            }
        ]
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        req_id = req.get("id")
        params = req.get("params") or {}

        if req_id is None:
            # Notification (e.g., notifications/initialized)
            continue

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "dev-resource-hub", "version": "1.0.0"}
                }
            }
        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": TOOLS}
            }
        elif method == "tools/call":
            t_name = params.get("name", "")
            t_args = params.get("arguments") or {}
            result = handle_tool_call(t_name, t_args)
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": result
            }
        elif method == "ping":
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
