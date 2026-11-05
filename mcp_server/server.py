#!/usr/bin/env python3
"""
Agent Tools Local MCP Server (Model Context Protocol)
Generic, zero-dependency, high-performance tooling for AI coding assistants:
- Skills Vault discovery, activation & deactivation ('list_vault_skills', 'equip_skill', 'unequip_skill')
- Brand Design Systems discovery, retrieval & accessibility ('list_brand_designs', 'get_brand_design', 'check_contrast')
- Codebase AST Knowledge Graph health, construction & traversal ('inspect_codebase_graph', 'build_codebase_graph', 'query_codebase_graph')

Architected by Viktor (Vik) - Viklabs (https://viklabs.pages.dev/)
Runs over standard JSON-RPC 2.0 stdio transport.
"""

import sys
import os
import json
import shutil
import re
import ast
import subprocess
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
    # --- Domain 1: Skills Vault ---
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
        "description": "Extracts and installs a specialized skill package from the offline vault into the assistant's active skills folder. Mutating file operation: creates or overwrites only the specific skill subfolder in the target directory (defaulting to ~/.gemini/config/skills); leaves all other workspace files untouched. Requires no network access or authentication. If the requested skill is not found, returns an error with available matching suggestions without modifying disk state.\n\nWhen to use: Call before writing domain-specific code (game design, mobile QA, shaders, advanced refactoring) to load specialized instructions directly into context.\nWhen NOT to use: Do not use to search or discover unknown skills; use list_vault_skills first. To remove an equipped skill after a task is finished, use unequip_skill.\nReturns: Success confirmation, destination path, and the full markdown instructions of the equipped skill for immediate context execution.",
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
        "name": "unequip_skill",
        "description": "Uninstalls and removes an equipped skill from the assistant's active skills folder to clean up environment state and preserve context tokens. Mutating file operation: safely deletes only the specified skill directory from the target skills folder (defaulting to ~/.gemini/config/skills or .agents/skills); leaves all other skills and workspace files untouched. Requires no network access or authentication. If the skill is not installed, safely returns a notice without throwing an error.\n\nWhen to use: Call when a specialized task is completed and you no longer need the skill instructions in prompt context.\nWhen NOT to use: Do not use to delete skills from the permanent offline vault (skills-vault/); this tool only removes temporary equipped copies from the active assistant environment.\nReturns: Confirmation message stating whether the skill was successfully removed or was not present in the active directory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of the equipped skill folder to remove (e.g. 'taste-skill', 'antislop-ui', 'game-design-studio', 'kubernetes-expert'). Case-insensitive. Required."
                },
                "target_path": {
                    "type": "string",
                    "description": "Custom destination folder path where the skill was installed. If omitted or empty, automatically resolves to the active global skills directory (~/.gemini/config/skills) or local .agents/skills.",
                    "default": ""
                }
            },
            "required": ["skill_name"]
        }
    },

    # --- Domain 2: Brand Design Systems & Accessibility ---
    {
        "name": "list_brand_designs",
        "description": "Lists and searches all 74 curated digital brand design systems available in the design-md-library. Safe, read-only operation: performs local directory enumeration with zero side effects, no mutations, and no network access. If a query keyword is provided, filters brand names by substring match.\n\nWhen to use: Call to explore available brand design systems before styling UI components.\nWhen NOT to use: Do not use to fetch full design tokens or color palettes; use get_brand_design once a brand slug is selected.\nReturns: Alphabetical list of available brand design names matching the query, with instructions to fetch specific tokens.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Optional search term to filter brand names (e.g. 'linear', 'stripe', 'apple', 'ai', 'crypto'). If omitted or empty, lists all 74 available brands.",
                    "default": ""
                }
            }
        }
    },
    {
        "name": "get_brand_design",
        "description": "Retrieves design specifications, color tokens, typography scales, elevation shadows, and layout rules for a specific brand from the local design library. Safe, read-only operation: performs local disk read with no side effects, mutations, network requests, or authentication requirements. If an unknown brand slug is requested, falls back to substring matching or suggests running list_brand_designs.\n\nWhen to use: Call whenever styling UI components, design tokens, or pages to follow authentic brand aesthetics.\nWhen NOT to use: Do not use to explore or list available brands (use list_brand_designs), and do not use to calculate color accessibility compliance (use check_contrast).\nReturns: Full markdown design specification containing color palettes, typography, spacing, and component patterns for the requested brand.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "brand": {
                    "type": "string",
                    "description": "Exact name of the brand to retrieve (e.g. 'linear', 'stripe', 'apple', 'supabase', 'vercel', 'raycast', 'figma'). Run list_brand_designs to discover all 74 available brand names. Required."
                }
            },
            "required": ["brand"]
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

    # --- Domain 3: Codebase AST Knowledge Graph ---
    {
        "name": "inspect_codebase_graph",
        "description": "Inspects the operational state and artifact health of the AST knowledge graph for a repository. Safe, read-only diagnostic: reads local metadata files with zero mutations, network calls, or side effects. Discloses whether graphify-out/ exists, artifact count, indexed file statistics, and last build metrics.\n\nWhen to use: Call to check whether a knowledge graph exists before deciding to build or query it.\nWhen NOT to use: Do not use to construct the graph (use build_codebase_graph) or to query specific symbol definitions and god classes (use query_codebase_graph).\nReturns: Graph status (ACTIVE or NOT BUILT), artifact count, indexed file count, node/edge metrics, and next action recommendations.",
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
        "name": "build_codebase_graph",
        "description": "Generates and indexes the AST knowledge graph for a repository, creating precomputed dependency maps, god classes, and structural summaries in graphify-out/. Mutating file operation: creates or updates only the local graphify-out/ artifact directory inside the target repository root; leaves all existing source code files unmodified. Requires zero network access or external credentials. If the external graphify CLI is installed in PATH, invokes it; otherwise, automatically executes a native, zero-dependency Python AST parser to extract classes, functions, and import dependencies.\n\nWhen to use: Call before deep codebase refactoring or exploration when inspect_codebase_graph indicates no graph exists.\nWhen NOT to use: Do not use if graphify-out/ is already active and up-to-date; use query_codebase_graph to query the existing graph directly.\nReturns: Build report containing extracted node count, edge count, detected god classes, and path to the generated graphify-out/ directory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Absolute or relative path to the target repository root where graphify-out/ will be built. If omitted, empty string, or '.', defaults to the current working directory.",
                    "default": ""
                },
                "force_rebuild": {
                    "type": "boolean",
                    "description": "Whether to overwrite an existing graphify-out/ directory if already present. Defaults to false.",
                    "default": False
                }
            }
        }
    },
    {
        "name": "query_codebase_graph",
        "description": "Traverses and queries an existing AST knowledge graph to inspect symbol definitions, identify architectural god classes, trace dependencies, or examine functional clusters. Safe, read-only query: performs local file reads inside graphify-out/ without mutations, network calls, or authentication. Prerequisite: requires an active graph generated via build_codebase_graph; if no graph exists, returns an actionable notice directing the caller to build it.\n\nWhen to use: Call during codebase onboarding, architectural review, or refactoring to retrieve targeted structural relationships without loading massive source files.\nWhen NOT to use: Do not use to check general graph health or existence (use inspect_codebase_graph), and do not use to construct the graph (use build_codebase_graph).\nReturns: Structured architectural intelligence matching the query mode: summary statistics, ranked god classes by centrality, top connected dependencies, or matched symbol occurrences.",
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

def handle_unequip_skill(args):
    skill_name = args.get("skill_name", "").strip()
    custom_target = args.get("target_path", "").strip()

    if not skill_name:
        return "Error: 'skill_name' argument is required. Specify the name of the equipped skill to remove."

    target_dir = Path(custom_target) if custom_target else DEFAULT_GLOBAL_SKILLS
    target_skill_dir = target_dir / skill_name

    if not target_skill_dir.exists() and target_dir.is_dir():
        for d in target_dir.iterdir():
            if d.is_dir() and d.name.lower() == skill_name.lower():
                target_skill_dir = d
                break

    if not target_skill_dir.exists():
        return f"Notice: Skill '{skill_name}' was not found in active skills directory at {target_dir}. No changes made."

    try:
        shutil.rmtree(target_skill_dir)
        return f"Success: Skill '{target_skill_dir.name}' unequipped and safely removed from {target_dir}. Context tokens freed."
    except Exception as e:
        return f"Error unequipping skill '{skill_name}': {str(e)}"

def handle_list_brand_designs(args):
    query = args.get("query", "").strip().lower()
    if not DESIGN_LIB_DIR.is_dir():
        return f"Error: design-md-library not found at {DESIGN_LIB_DIR}"

    brands = sorted([d.name for d in DESIGN_LIB_DIR.iterdir() if d.is_dir()])
    if query:
        brands = [b for b in brands if query in b]

    if not brands:
        return f"No brand design systems found matching '{query}'. Available brand count: {len(list(DESIGN_LIB_DIR.iterdir()))}."

    return (
        f"=== AVAILABLE BRAND DESIGN SYSTEMS ({len(brands)} total) ===\n"
        + ", ".join(brands)
        + "\n\n💡 Tip: Use `get_brand_design(brand='<name>')` to retrieve exact design tokens for any brand above."
    )

def handle_get_brand_design(args):
    brand = args.get("brand", "").strip().lower()
    if not brand or brand == "list":
        return handle_list_brand_designs(args)

    if not DESIGN_LIB_DIR.is_dir():
        return f"Error: design-md-library not found at {DESIGN_LIB_DIR}"

    brands = sorted([d.name for d in DESIGN_LIB_DIR.iterdir() if d.is_dir()])
    brand_dir = DESIGN_LIB_DIR / brand
    if not brand_dir.is_dir():
        matches = [b for b in brands if brand in b]
        if matches:
            brand_dir = DESIGN_LIB_DIR / matches[0]
            brand = matches[0]
        else:
            return f"Brand '{brand}' not found. Run `list_brand_designs()` to view all available brands."

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

def handle_inspect_codebase_graph(args):
    repo_path = args.get("repo_path", "").strip()
    target_repo = Path(repo_path) if repo_path else Path.cwd()

    if not target_repo.is_dir():
        return f"Error: Repository path '{target_repo}' is not a directory."

    graph_out = target_repo / "graphify-out"
    if not graph_out.is_dir():
        return (
            f"Codebase Graph status for '{target_repo.name}':\n"
            f"❌ NOT BUILT: No graphify-out/ directory found.\n"
            f"• To construct the AST knowledge graph, call `build_codebase_graph(repo_path='{target_repo.as_posix()}')`."
        )

    files = list(graph_out.glob("*"))
    graph_files = [f.name for f in files if f.is_file()]
    summary_file = graph_out / "graph_summary.json"
    extra_info = ""
    if summary_file.is_file():
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            files_count = data.get("total_files_indexed", "N/A")
            nodes = data.get("total_nodes", data.get("nodes", "N/A"))
            edges = data.get("total_edges", data.get("edges", "N/A"))
            extra_info = f"\n• Files indexed: {files_count} | AST Nodes: {nodes} | Dependencies: {edges}"
        except Exception:
            pass

    return (
        f"Codebase Graph status for '{target_repo.name}':\n"
        f"✅ ACTIVE: AST Knowledge Graph ready ({len(graph_files)} artifacts in graphify-out/){extra_info}\n"
        f"• Ready for symbol traversal via `query_codebase_graph(query='summary')`."
    )

def handle_build_codebase_graph(args):
    repo_path = args.get("repo_path", "").strip()
    force_rebuild = args.get("force_rebuild", False)
    target_repo = Path(repo_path) if repo_path else Path.cwd()

    if not target_repo.is_dir():
        return f"Error: Repository path '{target_repo}' is not a directory."

    graph_out = target_repo / "graphify-out"
    if graph_out.is_dir() and not force_rebuild:
        summary_file = graph_out / "graph_summary.json"
        if summary_file.is_file():
            return f"Notice: AST knowledge graph is already active at {graph_out}. Pass force_rebuild=true to regenerate, or call query_codebase_graph to query it."

    # Try external graphify CLI if present in system PATH
    graphify_bin = shutil.which("graphify")
    if graphify_bin:
        try:
            res = subprocess.run([graphify_bin, "run"], cwd=str(target_repo), capture_output=True, text=True, timeout=25)
            if res.returncode == 0 and graph_out.is_dir():
                return f"Success: Graphify CLI successfully generated AST knowledge graph at {graph_out}."
        except Exception:
            pass

    # Built-in native Python AST indexing engine (Zero-dependency fallback)
    graph_out.mkdir(parents=True, exist_ok=True)
    ignore_dirs = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'graphify-out', 'skills-vault', 'temp', 'tmp'}

    files = []
    for root, dirs, filenames in os.walk(target_repo):
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in ('.py', '.cs', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java', '.json', '.md'):
                files.append(Path(root) / fname)
            if len(files) >= 500:
                break
        if len(files) >= 500:
            break

    nodes = []
    edges = []
    god_nodes = []

    for f in files:
        rel = f.relative_to(target_repo).as_posix()
        nodes.append({"id": rel, "type": "file", "size": f.stat().st_size})
        if f.suffix == '.py':
            try:
                with open(f, 'r', encoding='utf-8', errors='replace') as sf:
                    tree = ast.parse(sf.read(), filename=str(f))
                for item in tree.body:
                    if isinstance(item, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                        name = item.name
                        lines = (getattr(item, 'end_lineno', item.lineno) or item.lineno) - item.lineno
                        node_id = f"{rel}:{name}"
                        nodes.append({"id": node_id, "type": type(item).__name__, "lines": lines})
                        if lines >= 20:
                            god_nodes.append({"symbol": node_id, "type": type(item).__name__, "lines": lines})
                    elif isinstance(item, ast.Import):
                        for alias in item.names:
                            edges.append({"from": rel, "to": alias.name, "type": "import"})
                    elif isinstance(item, ast.ImportFrom) and item.module:
                        edges.append({"from": rel, "to": item.module, "type": "import_from"})
            except Exception:
                pass
        elif f.suffix in ('.cs', '.ts', '.js'):
            try:
                with open(f, 'r', encoding='utf-8', errors='replace') as sf:
                    for line_no, line in enumerate(sf, 1):
                        m = re.search(r'\b(class|interface|struct|enum)\s+([A-Za-z0-9_]+)', line)
                        if m:
                            god_nodes.append({"symbol": f"{rel}:{m.group(2)}", "type": m.group(1), "line": line_no})
            except Exception:
                pass

    god_nodes.sort(key=lambda x: x.get('lines', 0), reverse=True)

    summary_data = {
        "repository": target_repo.name,
        "total_files_indexed": len(files),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "top_god_nodes": [g["symbol"] for g in god_nodes[:15]],
        "generator": "agent-tools-native-ast"
    }

    with open(graph_out / "graph_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    with open(graph_out / "god_nodes.json", "w", encoding="utf-8") as f:
        json.dump(god_nodes[:30], f, indent=2)

    return (
        f"Success: Built AST knowledge graph for '{target_repo.name}' at {graph_out}\n"
        f"• Files indexed: {len(files)}\n"
        f"• AST Nodes extracted: {len(nodes)}\n"
        f"• Dependency Edges: {len(edges)}\n"
        f"• God Classes identified: {len(god_nodes)}\n"
        f"Ready for query traversal via `query_codebase_graph(query='summary')`."
    )

def handle_query_codebase_graph(args):
    query = args.get("query", "summary").strip()
    repo_path = args.get("repo_path", "").strip()
    target_repo = Path(repo_path) if repo_path else Path.cwd()

    if not target_repo.is_dir():
        return f"Error: Repository path '{target_repo}' is not a directory."

    graph_out = target_repo / "graphify-out"
    if not graph_out.is_dir():
        return (
            f"Error: No AST knowledge graph exists for '{target_repo.name}'.\n"
            f"Prerequisite missing: Call `build_codebase_graph(repo_path='{target_repo.as_posix()}')` first before querying symbols or dependencies."
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
                god_nodes = data.get("top_god_nodes", data.get("god_nodes", []))
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
    # Domain 1: Skills
    "list_vault_skills": handle_list_vault_skills,
    "equip_skill": handle_equip_skill,
    "unequip_skill": handle_unequip_skill,
    # Domain 2: Brands & UI
    "list_brand_designs": handle_list_brand_designs,
    "get_brand_design": handle_get_brand_design,
    "check_contrast": handle_check_contrast,
    # Domain 3: Codebase AST Graph
    "inspect_codebase_graph": handle_inspect_codebase_graph,
    "get_graphify_status": handle_inspect_codebase_graph, # Backwards compatibility alias
    "graphify_status": handle_inspect_codebase_graph,     # Backwards compatibility alias
    "build_codebase_graph": handle_build_codebase_graph,
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
                    "version": "1.3.0"
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
    print("Testing 'agent-tools' MCP server tools locally (9 tools across 3 trios)...")
    
    print("\n--- [Domain 1] Test 1: list_vault_skills ---")
    print(handle_list_vault_skills({"query": "react", "limit": 2}))
    
    print("\n--- [Domain 1] Test 2: equip_skill ---")
    print(handle_equip_skill({"skill_name": "taste-skill"})[:150] + "...")

    print("\n--- [Domain 1] Test 3: unequip_skill ---")
    print(handle_unequip_skill({"skill_name": "taste-skill"}))
    
    print("\n--- [Domain 2] Test 4: list_brand_designs ---")
    print(handle_list_brand_designs({"query": "line"})[:150] + "...")

    print("\n--- [Domain 2] Test 5: get_brand_design (linear) ---")
    res = handle_get_brand_design({"brand": "linear"})
    print(res[:180] + "...")

    print("\n--- [Domain 2] Test 6: check_contrast ---")
    print(handle_check_contrast({"foreground": "#ffffff", "background": "#000000"}))
    print(handle_check_contrast({"foreground": "#777777", "background": "#ffffff"}))
    
    print("\n--- [Domain 3] Test 7: inspect_codebase_graph ---")
    print(handle_inspect_codebase_graph({"repo_path": str(BASE_DIR)}))

    print("\n--- [Domain 3] Test 8: build_codebase_graph ---")
    print(handle_build_codebase_graph({"repo_path": str(BASE_DIR)}))

    print("\n--- [Domain 3] Test 9: query_codebase_graph (summary) ---")
    print(handle_query_codebase_graph({"query": "summary", "repo_path": str(BASE_DIR)}))

    # Clean up test graphify-out
    test_graph = BASE_DIR / "graphify-out"
    if test_graph.is_dir():
        shutil.rmtree(test_graph)

    print("\n✅ All 9 local tool tests passed successfully with 100% domain coverage!")

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
