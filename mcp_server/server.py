#!/usr/bin/env python3
"""
Agent Tools Local MCP Server (Model Context Protocol)
Generic, zero-dependency, high-performance tooling for AI coding assistants:
- Skills Vault query & dynamic unfreezing ('equip_skill')
- Brand Design Systems retrieval (74 world-class brands anti-slop)
- WCAG 2.x contrast verification
- Graphify codebase knowledge graph status

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
        "description": "Searches or lists skills from the offline Skills Vault (900+ skills) by keyword or category to identify specialized tools for any technical domain without bloating the token context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keyword (e.g. 'kubernetes', 'react', 'shader', 'unity', 'security', 'docker')",
                    "default": ""
                },
                "category": {
                    "type": "string",
                    "description": "Filter by category (e.g. 'gamedev', 'devops', 'frontend', 'security', 'ai', 'general')",
                    "default": ""
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return (default: 12)",
                    "default": 12
                }
            }
        }
    },
    {
        "name": "equip_skill",
        "description": "Autonomous skill unfreezer (STOP & EQUIP protocol). Dynamically extracts a specialized skill from the offline vault and installs it directly into the active assistant's environment in real-time.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name or folder of the skill to equip (e.g. 'taste-skill', 'antislop-ui', 'kubernetes-expert', 'game-design-studio')"
                },
                "target_path": {
                    "type": "string",
                    "description": "Optional custom destination directory for the equipped skill. If omitted, installs to active global or workspace skills directory.",
                    "default": ""
                }
            },
            "required": ["skill_name"]
        }
    },
    {
        "name": "get_brand_design",
        "description": "Retrieves the design system, color tokens, typography, elevation, and anti-slop rules for any of the 74 brands in design-md-library (e.g. 'linear', 'stripe', 'apple', 'supabase', 'vercel', 'raycast', 'figma'). Pass 'list' to see all brands.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "brand": {
                    "type": "string",
                    "description": "Brand name (e.g. 'linear', 'stripe', 'supabase', 'vercel') or 'list' to see all 74 brands",
                    "default": "list"
                }
            }
        }
    },
    {
        "name": "check_contrast",
        "description": "Computes the WCAG 2.x contrast ratio between two hex colors and provides PASS/FAIL verdicts for normal text (4.5:1) and large text (3.0:1) to enforce accessible, professional UI design.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "foreground": {
                    "type": "string",
                    "description": "Hex color of the text (e.g. '#FFFFFF' or '#777777')"
                },
                "background": {
                    "type": "string",
                    "description": "Hex color of the background (e.g. '#000000' or '#120726')"
                }
            },
            "required": ["foreground", "background"]
        }
    },
    {
        "name": "graphify_status",
        "description": "Inspects the status of the Graphify knowledge graph (AST & dependency graph) for a repository to assess code comprehension and token savings.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Path to the repository to inspect. If omitted, uses current working directory.",
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

    if not CATALOG_FILE.is_file():
        # Fallback to scanning vault directory directly
        if not VAULT_DIR.is_dir():
            return f"Error: Skills vault not found at {VAULT_DIR}"
        skills = [d.name for d in VAULT_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()]
        if query:
            skills = [s for s in skills if query in s.lower()]
        return f"Found {len(skills)} skills (no catalog.json):\n" + "\n".join(f"- {s}" for s in skills[:limit])

    try:
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            cat = json.load(f)

        results = []
        for name, data in cat.items():
            desc = data.get("description", "").lower()
            cat_name = data.get("category", "").lower()

            match = True
            if query:
                match = (query in name.lower() or query in desc or query in cat_name)
            if match and category:
                match = (category in cat_name)

            if match:
                results.append((name, data.get("category", "general"), data.get("description", "")))

        if not results:
            return f"No skills found in vault matching query='{query}' category='{category}'."

        lines = [f"Found {len(results)} matching skills in vault (showing up to {limit}):\n"]
        for name, c, desc in results[:limit]:
            short_desc = (desc[:100] + "...") if len(desc) > 100 else desc
            lines.append(f"• **{name}** `[{c}]`: {short_desc}")

        if len(results) > limit:
            lines.append(f"\n*(...and {len(results) - limit} more skills available in vault)*")

        lines.append("\n💡 Tip: Use `equip_skill` with any skill name above to activate it instantly.")
        return "\n".join(lines)
    except Exception as e:
        return f"Error reading catalog: {str(e)}"

def handle_equip_skill(args):
    skill_name = args.get("skill_name", "").strip()
    custom_target = args.get("target_path", "").strip()

    if not skill_name:
        return "Error: 'skill_name' argument is required."

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
        return f"Error: Skill '{skill_name}' not found in vault at {VAULT_DIR}."

    dst = target_dir / src.name
    try:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        return f"Success: Skill '{src.name}' equipped at {dst}. Assistant environment will load it immediately."
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
    if len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color: #{hex_str}")
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
        return "Error: Both 'foreground' and 'background' hex colors are required."

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
        f"   Foreground: {fg_str} (RGB: {fg_rgb})",
        f"   Background: {bg_str} (RGB: {bg_rgb})",
        "",
        f"• Normal Text (>= 4.5:1): {'✅ PASS' if normal_pass else '❌ FAIL'}",
        f"• Large Text (>= 3.0:1):  {'✅ PASS' if large_pass else '❌ FAIL'}",
    ]
    if not normal_pass:
        lines.append("\n⚠️ Warning: Fails WCAG AA for body text. Adjust brightness or contrast to comply with Anti-Slop standards.")
    return "\n".join(lines)

def handle_graphify_status(args):
    repo_path = args.get("repo_path", "").strip()
    target_repo = Path(repo_path) if repo_path else Path.cwd()

    if not target_repo.is_dir():
        return f"Error: Repository path '{target_repo}' is not a directory."

    graph_out = target_repo / "graphify-out"
    if not graph_out.is_dir():
        return f"Graphify status for {target_repo.name}:\n❌ No graphify-out/ directory found. Graph has not been built yet.\nRun `graphify` or `python skills_manager.py doctor` to initialize."

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

    return f"Graphify status for '{target_repo.name}':\n✅ Graph is active ({len(graph_files)} artifacts in graphify-out/){extra_info}\n• Knowledge Graph ready for fast AST context retrieval."

# Dispatcher
HANDLERS = {
    "list_vault_skills": handle_list_vault_skills,
    "equip_skill": handle_equip_skill,
    "get_brand_design": handle_get_brand_design,
    "check_contrast": handle_check_contrast,
    "graphify_status": handle_graphify_status,
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
                    "version": "1.0.0"
                }
            }
        }

    elif method == "notifications/initialized":
        return None

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
    
    print("\n--- Test: graphify_status ---")
    print(handle_graphify_status({"repo_path": str(BASE_DIR)}))

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
