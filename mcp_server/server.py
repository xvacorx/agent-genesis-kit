#!/usr/bin/env python3
"""
Agent Tools Local MCP Server (Model Context Protocol)
Generic, zero-dependency, high-performance tooling for AI coding assistants:
- Skills Vault discovery & dynamic unfreezing ('equip_skill' via STOP & EQUIP)
- Brand Design Systems retrieval (74 world-class brands anti-slop)
- WCAG 2.x mathematical contrast verification
- Graphify codebase AST knowledge graph status & query traversal

Architected by Viktor (Vik) - Viklabs (https://viklabs.pages.dev/)
Runs over standard JSON-RPC 2.0 stdio transport.
"""

import sys
import os
import json
import shutil
import re
from pathlib import Path

# Force UTF-8 on Windows terminal output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Base Paths (Relative to repository root)
BASE_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = BASE_DIR / "skills-vault"
CATALOG_FILE = VAULT_DIR / "catalog.json"
DESIGN_LIB_DIR = BASE_DIR / "design-md-library"

# Default target skills directory (Antigravity global or workspace fallback)
DEFAULT_GLOBAL_SKILLS = Path.home() / ".gemini" / "config" / "skills"

TOOLS = [
    {
        "name": "list_vault_skills",
        "description": "Discovers and searches specialized skills from the offline Skills Vault (915+ skills) by keyword or domain category without bloating token context. Call this tool first to locate relevant skill names before invoking equip_skill. Returns matching skill entries with name, category, and capability summary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term or keyword to match against skill names and descriptions (e.g. 'kubernetes', 'react', 'shader', 'unity', 'security', 'docker'). If empty, returns skills within the specified category or top general skills.",
                    "default": ""
                },
                "category": {
                    "type": "string",
                    "description": "Optional domain category filter. Allowed values: 'gamedev', 'devops', 'frontend', 'security', 'ai', 'general', 'database', 'testing'. If omitted, searches across all categories.",
                    "default": ""
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of skill results to return (integer between 1 and 50). Defaults to 12 to preserve prompt tokens.",
                    "default": 12
                }
            }
        }
    },
    {
        "name": "equip_skill",
        "description": "Dynamically unfreezes and installs a specialized skill from the 915+ offline vault into the active assistant environment (STOP & EQUIP protocol). Call this tool whenever a task requires specialized domain knowledge, workflows, or rules (e.g. game design, anti-slop UI, Kubernetes, advanced debugging) before writing code. Returns the complete skill instruction markdown and destination path for immediate in-context execution. If a skill name is uncertain, call list_vault_skills first.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Exact name or folder of the skill to equip (e.g. 'taste-skill', 'antislop-ui', 'game-design-studio', 'csharp-pro', 'unity-6-mobile-master', 'kubernetes-expert'). Can be identified via list_vault_skills."
                },
                "target_path": {
                    "type": "string",
                    "description": "Optional absolute or relative path to the destination skills folder. If omitted, installs to the user's active global skills cache (~/.gemini/config/skills) or local workspace (.agents/skills).",
                    "default": ""
                }
            },
            "required": ["skill_name"]
        }
    },
    {
        "name": "get_brand_design",
        "description": "Retrieves comprehensive design system specifications, color tokens, typography scales, elevation shadows, and anti-slop aesthetic rules from 74 world-class digital brands (design-md-library). Call this tool whenever styling user interfaces, web apps, or frontend components to deliver production-grade design instead of generic AI slop. Returns the brand's full markdown design tokens or an index of available brands if 'list' is passed.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "brand": {
                    "type": "string",
                    "description": "Brand slug identifier (e.g. 'linear', 'stripe', 'apple', 'supabase', 'vercel', 'raycast', 'figma', 'notion') to fetch its design tokens, or 'list' to view all 74 indexed brand design systems.",
                    "default": "list"
                }
            }
        }
    },
    {
        "name": "check_contrast",
        "description": "Computes the mathematical WCAG 2.x relative luminance contrast ratio between foreground text and background colors, returning PASS/FAIL verdicts for normal text (ratio >= 4.5:1) and large/bold text (ratio >= 3.0:1). Call this tool whenever selecting color pairs for UI elements, text, buttons, or badges to prevent unreadable, inaccessible designs and enforce Anti-Slop quality standards. Returns the exact ratio, RGB conversion, WCAG AA compliance verdicts, and adjustment recommendations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "foreground": {
                    "type": "string",
                    "description": "Hex color code for the foreground text or icon. Accepts 3-digit (#fff) or 6-digit (#ffffff) hex strings, with or without leading '#' (e.g. '#FFFFFF', 'f97316', '#38bdf8')."
                },
                "background": {
                    "type": "string",
                    "description": "Hex color code for the surface or background container. Accepts 3-digit (#000) or 6-digit (#08090a) hex strings, with or without leading '#' (e.g. '#08090a', '#181726', '#000000')."
                }
            },
            "required": ["foreground", "background"]
        }
    },
    {
        "name": "get_graphify_status",
        "description": "Inspects the operational state and artifact health of the Graphify AST knowledge graph for a repository. Call this tool before analyzing or refactoring codebases to verify if precomputed dependency graphs, AST god classes, and community clusters exist, enabling up to 80% token reduction during code exploration. Returns active graph status, node/edge metrics, artifact count, and recommended next steps.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Absolute or relative path to the target repository root to inspect. If omitted or empty, inspects the current working directory.",
                    "default": ""
                }
            }
        }
    },
    {
        "name": "query_codebase_graph",
        "description": "Queries the codebase AST knowledge graph to inspect symbol definitions, identify architectural god classes, trace file dependencies, or search community clusters without reading massive source files. Call this tool during codebase onboarding, architectural review, or debugging to retrieve targeted structural relationships with minimal token usage. Returns matched graph nodes, dependency edges, god class rankings, or architectural structure summary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query target or operation mode: enter a class/function/symbol name to look up, or one of the special commands: 'summary' (overall architecture & metrics), 'god_nodes' (classes with highest complexity/dependencies), 'dependencies' (top connected modules), or 'communities' (detected functional clusters).",
                    "default": "summary"
                },
                "repo_path": {
                    "type": "string",
                    "description": "Absolute or relative path to the repository containing graphify-out/. If omitted or empty, queries the current working directory.",
                    "default": ""
                }
            }
        }
    }
]

# --- Handlers ---

def handle_list_vault_skills(args):
    query = args.get("query", "").strip().lower()
    category = args.get("category", "").strip().lower()
    limit = args.get("limit", 12)
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        limit = 12

    if not CATALOG_FILE.is_file():
        if not VAULT_DIR.is_dir():
            return f"Error: Skills vault not found at {VAULT_DIR}"
        skills = sorted([d.name for d in VAULT_DIR.iterdir() if d.is_dir()])
        if query:
            skills = [s for s in skills if query in s.lower()]
        return f"Skills Vault ({len(skills)} matching):\n• " + "\n• ".join(skills[:limit])

    try:
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        results = []
        for name, data in catalog.items():
            cat = data.get("category", "general").lower()
            desc = data.get("description", "").lower()
            folder = data.get("folder", name).lower()

            if category and category not in cat:
                continue

            if query:
                if query not in name.lower() and query not in desc and query not in folder:
                    continue

            results.append((name, data.get("category", "general"), data.get("description", "")))

        if not results:
            return f"No skills found in vault matching query='{query}' category='{category}'. Try broader terms like 'react', 'unity', 'docker', or call with empty query to browse."

        lines = [f"=== SKILLS VAULT DISCOVERY ({len(results)} found, showing top {min(limit, len(results))}) ===\n"]
        for name, c, d in results[:limit]:
            short_desc = (d[:100] + "...") if len(d) > 100 else d
            lines.append(f"• **{name}** `[{c}]`: {short_desc}")

        if len(results) > limit:
            lines.append(f"\n*(...and {len(results) - limit} more skills available in vault)*")

        lines.append("\n💡 Tip: Use `equip_skill(skill_name='<name>')` with any skill above to activate it instantly.")
        return "\n".join(lines)
    except Exception as e:
        return f"Error reading catalog: {str(e)}"

def handle_equip_skill(args):
    skill_name = args.get("skill_name", "").strip()
    custom_target = args.get("target_path", "").strip()

    if not skill_name:
        return "Error: 'skill_name' argument is required. Call list_vault_skills first to find valid names."

    target_dir = Path(custom_target) if custom_target else DEFAULT_GLOBAL_SKILLS
    target_dir.mkdir(parents=True, exist_ok=True)

    src = VAULT_DIR / skill_name
    if not src.is_dir() and CATALOG_FILE.is_file():
        try:
            with open(CATALOG_FILE, "r", encoding="utf-8") as f:
                cat = json.load(f)
            if skill_name in cat:
                folder = cat[skill_name].get("folder", skill_name)
                src = VAULT_DIR / folder
            else:
                for k, v in cat.items():
                    if skill_name.lower() in k.lower() or skill_name.lower() in v.get("name", "").lower():
                        folder = v.get("folder", k)
                        if (VAULT_DIR / folder).is_dir():
                            src = VAULT_DIR / folder
                            break
        except Exception:
            pass

    if not src.is_dir():
        return f"Error: Skill '{skill_name}' not found in vault at {VAULT_DIR}. Run `list_vault_skills(query='{skill_name}')` to search available skills."

    dst = target_dir / src.name
    try:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        preview = ""
        skill_md = dst / "SKILL.md"
        if skill_md.is_file():
            try:
                with open(skill_md, "r", encoding="utf-8", errors="replace") as sf:
                    preview = "\n\n=== EQUIPPED SKILL INSTRUCTIONS ===\n" + sf.read()[:2000]
            except Exception:
                pass

        return f"Success: Skill '{src.name}' equipped at {dst}. Assistant environment will load it immediately.{preview}"
    except Exception as e:
        return f"Error equipping skill '{src.name}': {str(e)}"

def handle_get_brand_design(args):
    brand = args.get("brand", "list").strip().lower()
    if not DESIGN_LIB_DIR.is_dir():
        return f"Error: design-md-library not found at {DESIGN_LIB_DIR}"

    brands = sorted([d.name for d in DESIGN_LIB_DIR.iterdir() if d.is_dir()])

    if brand == "list" or not brand:
        return f"Available Brand Design Systems ({len(brands)} total):\n" + ", ".join(brands)

    brand_dir = DESIGN_LIB_DIR / brand
    if not brand_dir.is_dir():
        matches = [b for b in brands if brand in b]
        if matches:
            brand_dir = DESIGN_LIB_DIR / matches[0]
            brand = matches[0]
        else:
            return f"Brand '{brand}' not found. Available brands: " + ", ".join(brands[:25]) + "..."

    design_file = brand_dir / "DESIGN.md"
    if not design_file.is_file():
        return f"Error: DESIGN.md missing in {brand_dir}"

    try:
        with open(design_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return f"=== DESIGN SYSTEM: {brand.upper()} ===\n\n" + content
    except Exception as e:
        return f"Error reading {design_file}: {str(e)}"

def parse_hex_color(hex_str):
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) == 8:
        hex_str = hex_str[:6]
    elif len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])
    elif len(hex_str) == 4:
        hex_str = "".join([c * 2 for c in hex_str[:3]])
    if len(hex_str) != 6 or not re.match(r"^[0-9a-fA-F]{6}$", hex_str):
        raise ValueError(f"Invalid hex color: #{hex_str}. Expected 3 or 6 hex digits (e.g. '#FFFFFF', '#08090a').")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    srgb = [c / 255.0 for c in rgb]
    lum = []
    for c in srgb:
        if c <= 0.03928:
            lum.append(c / 12.92)
        else:
            lum.append(((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * lum[0] + 0.7152 * lum[1] + 0.0722 * lum[2]

def handle_check_contrast(args):
    fg_str = args.get("foreground", "").strip()
    bg_str = args.get("background", "").strip()

    if not fg_str or not bg_str:
        return "Error: Both 'foreground' and 'background' hex colors are required. Example: foreground='#FFFFFF', background='#08090a'."

    try:
        fg_rgb = parse_hex_color(fg_str)
        bg_rgb = parse_hex_color(bg_str)
    except ValueError as ve:
        return f"Error: {str(ve)}"

    l1 = relative_luminance(fg_rgb)
    l2 = relative_luminance(bg_rgb)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    ratio = (lighter + 0.05) / (darker + 0.05)

    normal_pass = ratio >= 4.5
    large_pass = ratio >= 3.0

    lines = [
        f"🎨 WCAG 2.x Contrast Ratio: {ratio:.2f}:1",
        f"   Foreground: #{''.join(f'{c:02X}' for c in fg_rgb)} (RGB: {fg_rgb})",
        f"   Background: #{''.join(f'{c:02X}' for c in bg_rgb)} (RGB: {bg_rgb})",
        "",
        f"• Normal Text (>= 4.5:1): {'✅ PASS (WCAG AA Compliant)' if normal_pass else '❌ FAIL (Insufficient contrast)'}",
        f"• Large Text (>= 3.0:1):  {'✅ PASS (WCAG AA Large Compliant)' if large_pass else '❌ FAIL (Insufficient contrast)'}",
    ]
    if not normal_pass:
        lines.append("\n⚠️ Anti-Slop Alert: Ratio is below 4.5:1 for body copy. Darken background or increase foreground luminance to ensure readability.")
    return "\n".join(lines)

def handle_get_graphify_status(args):
    repo_path = args.get("repo_path", "").strip()
    target_repo = Path(repo_path) if repo_path else Path.cwd()

    if not target_repo.is_dir():
        return f"Error: Repository path '{target_repo}' is not a directory."

    graph_out = target_repo / "graphify-out"
    if not graph_out.is_dir():
        return (
            f"Graphify status for '{target_repo.name}':\n"
            f"❌ No graphify-out/ directory found. AST knowledge graph has not been built yet.\n"
            f"• To build AST graph and unlock 80% token savings, run `graphify` in the terminal."
        )

    files = list(graph_out.glob("*"))
    graph_files = [f.name for f in files if f.is_file()]
    summary_file = graph_out / "graph_summary.json"
    extra_info = ""
    if summary_file.is_file():
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            nodes = data.get("nodes", data.get("total_nodes", "N/A"))
            edges = data.get("edges", data.get("total_edges", "N/A"))
            extra_info = f"\n• Nodes: {nodes} | Edges: {edges}"
        except Exception:
            pass

    return (
        f"Graphify status for '{target_repo.name}':\n"
        f"✅ Knowledge Graph is ACTIVE ({len(graph_files)} artifacts in graphify-out/){extra_info}\n"
        f"• Ready for AST queries via `query_codebase_graph(query='summary')`."
    )

def handle_query_codebase_graph(args):
    query = args.get("query", "summary").strip()
    repo_path = args.get("repo_path", "").strip()
    target_repo = Path(repo_path) if repo_path else Path.cwd()

    if not target_repo.is_dir():
        return f"Error: Repository path '{target_repo}' is not a directory."

    graph_out = target_repo / "graphify-out"
    if not graph_out.is_dir():
        files = [p for p in target_repo.iterdir() if not p.name.startswith(".")]
        dirs = [p.name for p in files if p.is_dir()]
        code_files = [p.name for p in files if p.is_file() and p.suffix in (".py", ".cs", ".ts", ".js", ".go", ".rs", ".java", ".cpp", ".json", ".md")]
        return (
            f"=== CODEBASE ARCHITECTURE SCAN: '{target_repo.name}' ===\n"
            f"ℹ️ Precomputed graphify-out/ not found. Showing lightweight architectural structure:\n"
            f"• Top Directories ({len(dirs)}): {', '.join(dirs[:12])}\n"
            f"• Root Code Files ({len(code_files)}): {', '.join(code_files[:12])}\n\n"
            f"💡 To build full AST dependency graph and enable god_nodes/communities queries, run:\n"
            f"   graphify\n"
            f"   (or run: python skills_manager.py doctor)"
        )

    summary_file = graph_out / "graph_summary.json"
    god_nodes_file = graph_out / "god_nodes.json"
    graph_json = graph_out / "graph.json"
    graph_index = graph_out / "index.json"

    q_lower = query.lower()

    if q_lower in ("god_nodes", "god-nodes", "godclasses", "centrality"):
        if god_nodes_file.is_file():
            try:
                with open(god_nodes_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return f"=== GOD NODES (Highest Centrality & Complexity) ===\n\n" + json.dumps(data, indent=2)[:3000]
            except Exception as e:
                return f"Error reading god_nodes.json: {str(e)}"
        elif summary_file.is_file():
            try:
                with open(summary_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                god_nodes = data.get("god_nodes", data.get("top_central_nodes", []))
                if god_nodes:
                    return f"=== GOD NODES DETECTED ===\n" + "\n".join([f"• {n}" for n in god_nodes[:15]])
            except Exception:
                pass
        return "No specific god_nodes file found in graphify-out/. Try query='summary'."

    if q_lower in ("summary", "overview", "stats"):
        if summary_file.is_file():
            try:
                with open(summary_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return f"=== KNOWLEDGE GRAPH SUMMARY: '{target_repo.name}' ===\n\n" + json.dumps(data, indent=2)[:3000]
            except Exception as e:
                return f"Error reading graph_summary.json: {str(e)}"
        artifacts = [f.name for f in graph_out.iterdir() if f.is_file()]
        return f"=== GRAPHIFY ARTIFACTS: '{target_repo.name}' ===\nAvailable graph artifacts:\n• " + "\n• ".join(artifacts)

    # Search keyword across graph files
    found_matches = []
    target_files = [graph_json, summary_file, god_nodes_file, graph_index]
    for tf in target_files:
        if tf and tf.is_file():
            try:
                with open(tf, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        if q_lower in line.lower():
                            found_matches.append(line.strip())
                            if len(found_matches) >= 15:
                                break
            except Exception:
                pass
        if len(found_matches) >= 15:
            break

    if found_matches:
        return f"=== GRAPH SEARCH MATCHES FOR '{query}' ===\n" + "\n".join(found_matches[:15])

    return (
        f"Query '{query}' completed on graphify-out/ for '{target_repo.name}'.\n"
        f"No direct node match found. Try querying 'summary', 'god_nodes', or a broader class name."
    )

# Dispatcher (Includes backwards compatibility aliases)
HANDLERS = {
    "list_vault_skills": handle_list_vault_skills,
    "equip_skill": handle_equip_skill,
    "get_brand_design": handle_get_brand_design,
    "check_contrast": handle_check_contrast,
    "get_graphify_status": handle_get_graphify_status,
    "graphify_status": handle_get_graphify_status, # Backwards compatibility alias
    "query_codebase_graph": handle_query_codebase_graph,
}

def handle_json_rpc(line):
    try:
        req = json.loads(line)
    except json.JSONDecodeError:
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": "Parse error"}
        }

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "agent-tools",
                    "version": "1.1.0"
                }
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name not in HANDLERS:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }

        try:
            handler = HANDLERS[tool_name]
            result_text = handler(args)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": str(result_text)
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Execution error in {tool_name}: {str(e)}"
                        }
                    ],
                    "isError": True
                }
            }

    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }

def run_tests():
    print("Testing 'agent-tools' MCP server tools locally...")
    
    print("\n--- Test: list_vault_skills ---")
    print(handle_list_vault_skills({"query": "react", "limit": 3}))
    
    print("\n--- Test: check_contrast ---")
    print(handle_check_contrast({"foreground": "#ffffff", "background": "#000000"}))
    print(handle_check_contrast({"foreground": "#777777", "background": "#ffffff"}))
    
    print("\n--- Test: get_brand_design (list) ---")
    print(handle_get_brand_design({"brand": "list"})[:200] + "...")
    
    print("\n--- Test: get_brand_design (linear) ---")
    res = handle_get_brand_design({"brand": "linear"})
    print(res[:250] + "...")
    
    print("\n--- Test: get_graphify_status ---")
    print(handle_get_graphify_status({"repo_path": str(BASE_DIR)}))

    print("\n--- Test: query_codebase_graph (summary) ---")
    print(handle_query_codebase_graph({"query": "summary", "repo_path": str(BASE_DIR)}))

    print("\n✅ All local tool tests passed successfully!")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
        return

    # Standard JSON-RPC stdio loop
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        resp = handle_json_rpc(line)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
