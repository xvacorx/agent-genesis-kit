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
        "description": "Searches and enumerates specialized skills from the offline vault (915+ skills) by keyword or category. Safe, read-only operation: reads local catalog.json with zero side effects, no mutations, and no network access. When query and category are both provided, applies a logical AND filter. When both are omitted or empty, returns the top general engineering skills up to the specified limit. If no skills match, returns a helpful message with suggested search keywords.\n\nWhen to use: Call to discover skill names and capabilities before installation.\nWhen NOT to use: Do not use to install or execute skills; call equip_skill once a specific skill name is chosen.\nReturns: Formatted list of matching skills containing name, category tag, and summary description, plus remaining match count.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term matched case-insensitively against skill names, folder paths, and descriptions (e.g. 'react', 'unity', 'docker', 'shader', 'kubernetes'). Empty string matches all skills.",
                    "default": ""
                },
                "category": {
                    "type": "string",
                    "description": "Domain filter. Allowed values: 'gamedev', 'devops', 'frontend', 'security', 'ai', 'general', 'database', 'testing'. Combined with query using logical AND. Empty string searches across all categories.",
                    "default": ""
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of skill entries to return in a single call (integer from 1 to 50). Defaults to 12 to conserve context tokens.",
                    "default": 12
                }
            }
        }
    },
    {
        "name": "equip_skill",
        "description": "Extracts and installs a specialized skill package from the offline vault into the assistant's active skills folder. Mutating file operation: creates or overwrites only the specific skill subfolder in the target directory (defaulting to ~/.gemini/config/skills); leaves all other workspace files untouched. Requires no network access or authentication. If the requested skill is not found, returns an error with available matching suggestions without modifying disk state.\n\nWhen to use: Call before writing domain-specific code (game design, mobile QA, shaders, advanced refactoring) to load specialized instructions directly into context.\nWhen NOT to use: Do not use to search or discover unknown skills; use list_vault_skills first.\nReturns: Success confirmation, destination path, and the full markdown instructions of the equipped skill for immediate context execution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Exact folder or catalog slug of the skill to equip (e.g. 'taste-skill', 'game-design-studio', 'csharp-pro', 'unity-6-mobile-master'). Case-insensitive; if an approximate name is given, matches against catalog index. Required."
                },
                "target_path": {
                    "type": "string",
                    "description": "Custom destination folder path. If omitted or empty, automatically resolves to active global skills directory (~/.gemini/config/skills) or local .agents/skills.",
                    "default": ""
                }
            },
            "required": ["skill_name"]
        }
    },
    {
        "name": "get_brand_design",
        "description": "Retrieves design specifications, color tokens, typography scales, elevation shadows, and layout rules for 74 digital brands from the local design library. Safe, read-only operation: performs local disk read with no side effects, mutations, network requests, or authentication requirements. If an unknown brand slug is requested, falls back to substring matching or returns an alphabetical index of available brands.\n\nWhen to use: Call whenever styling UI components, design tokens, or pages to follow authentic brand aesthetics.\nWhen NOT to use: Do not use to calculate color accessibility compliance; use check_contrast to validate contrast ratios of retrieved colors.\nReturns: Full markdown design specification containing color palettes, typography, spacing, and component patterns; or a comma-separated index of all 74 brand names when brand='list'.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "brand": {
                    "type": "string",
                    "description": "Lowercase brand slug (e.g. 'linear', 'stripe', 'apple', 'supabase', 'vercel', 'raycast', 'figma'). Pass 'list' or empty string to retrieve all 74 available brand slugs. Defaults to 'list'.",
                    "default": "list"
                }
            }
        }
    },
    {
        "name": "check_contrast",
        "description": "Computes mathematical WCAG 2.x relative luminance contrast ratio between foreground and background colors. Non-destructive, read-only computation with no side effects, network access, or authentication. Automatically normalizes 3-digit hex (#fff -> #ffffff), 6-digit hex, and 8-digit hex (ignoring alpha). On malformed hex input, returns a descriptive error specifying expected hexadecimal syntax without throwing unhandled exceptions.\n\nWhen to use: Call whenever selecting color pairs for text, UI containers, buttons, or badges to verify WCAG AA compliance (>= 4.5:1 for normal body text, >= 3.0:1 for large or bold text >= 18pt).\nWhen NOT to use: Do not use for retrieving comprehensive brand styling or palettes; use get_brand_design instead.\nReturns: Mathematical ratio (e.g. 21.00:1), RGB conversions, PASS/FAIL verdicts for normal and large text, and luminance adjustment suggestions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "foreground": {
                    "type": "string",
                    "description": "Hex color for text or iconography. Accepts 3-digit (#fff), 6-digit (#ffffff), or 8-digit hex strings with or without leading '#'. Case-insensitive. Required."
                },
                "background": {
                    "type": "string",
                    "description": "Hex color for surface or container. Accepts 3-digit (#000), 6-digit (#08090a), or 8-digit hex strings with or without leading '#'. Case-insensitive. Required."
                }
            },
            "required": ["foreground", "background"]
        }
    },
    {
        "name": "get_graphify_status",
        "description": "Inspects the operational presence and artifact health of the Graphify AST knowledge graph for a repository. Safe, read-only diagnostic: reads local metadata files with zero mutations, network calls, or side effects. If no graph exists (graphify-out/ missing), safely returns a non-error status stating the graph is unbuilt and provides the command to generate it.\n\nWhen to use: Call before analyzing large codebases to determine if precomputed AST dependency graphs exist.\nWhen NOT to use: Do not use to query specific symbols, god classes, or module dependencies; use query_codebase_graph instead for graph traversal.\nReturns: Graph operational state (ACTIVE or NOT BUILT), artifact count, node/edge metrics if indexed, and actionable initialization instructions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Absolute or relative filesystem path to the target repository root. If omitted, empty string, or '.', defaults to the current working directory. Read-only access.",
                    "default": ""
                }
            }
        }
    },
    {
        "name": "query_codebase_graph",
        "description": "Traverses and searches the codebase AST knowledge graph to inspect symbol definitions, identify architectural god classes, trace dependencies, or examine functional clusters. Safe, read-only query: performs local file reads without mutations, network calls, or authentication. If the AST graph has not been precomputed (graphify-out/ missing), safely executes a non-failing structural fallback scan of top directories and code files with instructions to run graphify.\n\nWhen to use: Call during codebase onboarding, architectural review, or refactoring to retrieve targeted structural relationships without loading massive source files.\nWhen NOT to use: Do not use if you only need high-level graph health or existence; call get_graphify_status instead.\nReturns: Structured architectural intelligence matching the query mode: summary statistics, ranked god classes by centrality, top connected dependencies, or matched symbol occurrences.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Target symbol name (class, function, file) or operational keyword: 'summary' (overall metrics), 'god_nodes' (classes with highest centrality/complexity), 'dependencies' (top connected modules), or 'communities' (cluster breakdown). Case-insensitive. Defaults to 'summary'.",
                    "default": "summary"
                },
                "repo_path": {
                    "type": "string",
                    "description": "Absolute or relative path to the target repository root containing graphify-out/. If omitted, empty string, or '.', queries the current working directory.",
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
        lines.append("\n⚠️ Notice: Ratio is below 4.5:1 for body copy. Darken background or increase foreground luminance to ensure readability.")
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
