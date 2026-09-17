#!/usr/bin/env python3
"""
Skills Manager CLI & Engine for Agent Genesis Kit
Manage, search, activate, and deactivate skills from the offline Skills Vault (900+ skills)
and Brand Design Systems (74 DESIGN.md files) without overloading token context.

Architected with care by Viktor (Vik) - Viklabs (https://viklabs.pages.dev/)
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path

# Force UTF-8 on Windows terminal output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Core Base Paths
BASE_DIR = Path(__file__).resolve().parent
VAULT_DIR = BASE_DIR / "skills-vault"
DESIGN_LIB_DIR = BASE_DIR / "design-md-library"
CATALOG_FILE = VAULT_DIR / "catalog.json"
ACTIVE_PROFILE_FILE = BASE_DIR / "active_profile.json"

DEFAULT_GLOBAL_SKILLS = Path.home() / ".gemini" / "config" / "skills"

# Dynamic Profiles for System Prompt Token Diet
PROFILES = {
    "gamedev": {
        "name": "GameDev & Unity 6 Elite",
        "description": "Unity 6 Mobile, Zero-GC, Game Feel & Juiciness, Android QA, C# Pro, Systematic Debugging",
        "skills": [
            "unity-6-mobile-master",
            "game-feel-and-juiciness",
            "android-qa-playtesting",
            "unity-developer",
            "csharp-pro",
            "mobile-design",
            "systematic-debugging",
            "code-review",
            "self-improving-agent",
            "graphify",
        ]
    },
    "devops": {
        "name": "DevOps & Infrastructure Pro",
        "description": "Docker, Linux, Networking, Monitoring, Container Hardening, Systematic Debugging",
        "skills": [
            "docker-expert",
            "devops-troubleshooter",
            "linux-shell-scripting",
            "bash-pro",
            "network-engineer",
            "observability-monitoring-monitor-setup",
            "backend-security-coder",
            "python-pro",
            "systematic-debugging",
            "graphify",
        ]
    },
    "web": {
        "name": "Fullstack Web & Anti-Slop UI",
        "description": "Senior Frontend, UI Design System, React Best Practices, Modern Web Standards",
        "skills": [
            "senior-frontend",
            "ui-design-system",
            "antislop",
            "antislop-ui",
            "taste-skill",
            "react-best-practices",
            "design-md-catalog",
            "image-to-code-skill",
            "web-design-guidelines",
            "code-review",
            "self-improving-agent",
            "graphify",
        ]
    },
    "all-in-one": {
        "name": "Curated Elite Master Pack",
        "description": "Curated essential skills across GameDev, DevOps, Web & Core (< 2,200 tokens)",
        "skills": [
            "unity-6-mobile-master",
            "game-feel-and-juiciness",
            "csharp-pro",
            "docker-expert",
            "devops-troubleshooter",
            "senior-frontend",
            "ui-design-system",
            "antislop",
            "systematic-debugging",
            "code-review",
            "self-improving-agent",
            "graphify",
        ]
    },
    "core": {
        "name": "Minimal Core",
        "description": "Pure agentic core: Zero bloat (< 600 tokens) for general tasks",
        "skills": [
            "systematic-debugging",
            "code-review",
            "self-improving-agent",
            "antislop",
            "graphify",
        ]
    }
}

# Curated Bundles
BUNDLES = {
    "frontend-design-elite": {
        "description": "Elite anti-slop frontend suite, guidelines, and design systems",
        "skills": [
            "web-design-guidelines",
            "image-to-code-skill",
            "taste-skill",
            "react-best-practices",
            "design-md-catalog",
            "composition-patterns",
            "react-view-transitions",
            "minimalist-skill",
            "brutalist-skill",
            "soft-skill",
        ]
    },
    "fullstack-web": {
        "description": "Modern frontend, backend architecture, APIs, TypeScript, and UI systems",
        "skills": [
            "senior-frontend",
            "ui-design-system",
            "typescript-pro",
            "fastapi-pro",
            "backend-architect",
            "api-design-principles",
            "react-best-practices",
        ]
    },
    "security-audit": {
        "description": "Vulnerability scanning, secure coding, privilege and access audit",
        "skills": [
            "security-auditor",
            "api-security-best-practices",
            "backend-security-coder",
            "linux-privilege-escalation",
        ]
    }
}

def load_catalog():
    if not CATALOG_FILE.is_file():
        print(f"Warning: Catalog not found at {CATALOG_FILE}. Falling back to directory scan.")
        catalog = {}
        if VAULT_DIR.is_dir():
            for folder in VAULT_DIR.iterdir():
                if folder.is_dir() and (folder / "SKILL.md").exists():
                    catalog[folder.name] = {
                        "name": folder.name,
                        "folder": folder.name,
                        "description": f"Skill {folder.name}",
                        "category": "general"
                    }
        return catalog
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_target_dir(target=None, is_global=False):
    if is_global:
        return DEFAULT_GLOBAL_SKILLS
    if target:
        return Path(target).resolve()
    
    # Auto-detect local workspace .agents/skills
    local_skills = Path.cwd() / ".agents" / "skills"
    if local_skills.parent.exists():
        return local_skills
        
    return DEFAULT_GLOBAL_SKILLS

def resolve_skill_folder(skill_name, catalog):
    if (VAULT_DIR / skill_name).is_dir():
        return skill_name
    
    if skill_name in catalog:
        folder = catalog[skill_name].get("folder")
        if folder and (VAULT_DIR / folder).is_dir():
            return folder
            
    for k, v in catalog.items():
        if v.get("name") == skill_name or v.get("folder") == skill_name:
            folder = v.get("folder", k)
            if (VAULT_DIR / folder).is_dir():
                return folder

    for k, v in catalog.items():
        if skill_name.lower() in k.lower():
            folder = v.get("folder", k)
            if (VAULT_DIR / folder).is_dir():
                return folder

    return None

def search_skills(query, catalog):
    query = query.lower()
    results = []
    for name, data in catalog.items():
        desc = data.get("description", "").lower()
        cat = data.get("category", "").lower()
        if query in name.lower() or query in desc or query in cat:
            score = 0
            if query == name.lower():
                score += 100
            elif query in name.lower():
                score += 50
            if query in cat:
                score += 20
            if query in desc:
                score += 10
            results.append((score, data))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results]

def cmd_search(args, catalog):
    results = search_skills(args.query, catalog)
    print(f"\n🔍 Found {len(results)} skills matching '{args.query}':\n")
    for r in results[:args.limit]:
        print(f"  • \033[1m{r['name']}\033[0m ({r.get('category', 'general')}) [folder: {r.get('folder')}]")
        desc = r.get('description', '')
        if len(desc) > 120:
            desc = desc[:117] + "..."
        print(f"    {desc}\n")
    if len(results) > args.limit:
        print(f"  ... and {len(results) - args.limit} more. Use --limit to see more.")

def cmd_list(args, catalog):
    by_cat = {}
    for name, data in catalog.items():
        cat = data.get("category", "general")
        by_cat.setdefault(cat, []).append(name)
    
    print(f"\n📦 Skills Vault Catalog ({len(catalog)} total skills in {len(by_cat)} categories):\n")
    for cat in sorted(by_cat.keys()):
        skills = by_cat[cat]
        print(f"  \033[1m{cat}\033[0m ({len(skills)}): {', '.join(sorted(skills)[:8])}{'...' if len(skills) > 8 else ''}")
    print(f"\nUse 'python skills_manager.py search <query>' to explore.")

def copy_skill(folder_name, dest_dir):
    src = VAULT_DIR / folder_name
    dest = dest_dir / folder_name
    if not src.is_dir():
        print(f"  ❌ Skill folder not found: {src}")
        return False
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f"  ✅ Activated: {folder_name} -> {dest}")
    return True

def cmd_add(args, catalog):
    target = get_target_dir(args.target, args.global_install)
    print(f"\nTarget directory: {target}\n")
    
    for name in args.skills:
        folder = resolve_skill_folder(name, catalog)
        if folder:
            copy_skill(folder, target)
        else:
            print(f"  ❌ Unknown skill: '{name}'. Run 'search' to find matching names.")

def cmd_remove(args, catalog):
    target = get_target_dir(args.target, args.global_install)
    print(f"\nTarget directory: {target}\n")
    
    for name in args.skills:
        folder = resolve_skill_folder(name, catalog) or name
        dest = target / folder
        if dest.is_dir():
            shutil.rmtree(dest)
            print(f"  🗑️ Removed: {folder}")
        else:
            print(f"  ⚠️ Skill not currently active: {folder}")

def cmd_profile(args, catalog):
    profile_key = args.name.lower()
    if profile_key not in PROFILES:
        print(f"\n❌ Unknown profile '{args.name}'. Available profiles:")
        for k, v in PROFILES.items():
            print(f"  • {k}: {v['name']} ({len(v['skills'])} skills)")
        return
    
    prof = PROFILES[profile_key]
    target = get_target_dir(args.target, args.global_install)
    print(f"\n⚡ Activating Profile: \033[1m{prof['name']}\033[0m")
    print(f"   {prof['description']}")
    print(f"   Target: {target}\n")
    
    # Prune non-core skills if switching
    target.mkdir(parents=True, exist_ok=True)
    existing = [d.name for d in target.iterdir() if d.is_dir()]
    
    # Retain setup skills and core
    protected = {"agent-genesis"}
    for item in existing:
        if item not in prof["skills"] and item not in protected:
            shutil.rmtree(target / item)
            print(f"  🧹 Pruned: {item}")
            
    # Install profile skills
    for skill_name in prof["skills"]:
        folder = resolve_skill_folder(skill_name, catalog)
        if folder:
            copy_skill(folder, target)
        else:
            print(f"  ⚠️ Skill missing from vault: {skill_name}")
            
    # Save active profile metadata
    with open(ACTIVE_PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump({"active_profile": profile_key, "name": prof["name"]}, f, indent=2)
        
    print(f"\n🎉 Profile '{profile_key}' active with {len(prof['skills'])} skills deployed!\n")

def cmd_list_designs(args):
    if not DESIGN_LIB_DIR.is_dir():
        print(f"Design library not found at {DESIGN_LIB_DIR}")
        return
    brands = [d.name for d in sorted(DESIGN_LIB_DIR.iterdir()) if d.is_dir()]
    print(f"\n🎨 Brand Design Systems ({len(brands)} total brands available):\n")
    for b in brands:
        print(f"  • {b}")
    print(f"\nUse 'python skills_manager.py design <brand_name>' to view or copy.")

def cmd_design(args):
    brand = args.brand.lower()
    brand_dir = DESIGN_LIB_DIR / brand
    if not brand_dir.is_dir():
        matches = [d.name for d in DESIGN_LIB_DIR.iterdir() if d.is_dir() and brand in d.name.lower()]
        if matches:
            brand_dir = DESIGN_LIB_DIR / matches[0]
            brand = matches[0]
        else:
            print(f"❌ Brand '{args.brand}' not found. Run 'list-designs' to see all 74 brands.")
            return
            
    design_file = brand_dir / "DESIGN.md"
    if not design_file.is_file():
        print(f"❌ DESIGN.md missing in {brand_dir}")
        return
        
    if args.copy_to:
        dest = Path(args.copy_to).resolve()
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(design_file, dest)
        print(f"✅ Copied {brand} DESIGN.md to {dest}")
    else:
        print(f"\n📄 {brand.upper()} Design System Preview:\n" + "="*50)
        with open(design_file, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(30)]
            print("".join(lines))
        print("="*50 + f"\n... (Use --copy-to <path> to extract the full DESIGN.md)")

def cmd_sync(args, catalog):
    local_target = Path.cwd() / ".agents" / "skills"
    global_target = DEFAULT_GLOBAL_SKILLS
    
    print(f"\n🔄 Syncing active skills from Local -> Global cache ({global_target}):\n")
    if not local_target.is_dir():
        print("  Local .agents/skills does not exist in current directory.")
        return
        
def cmd_doctor(args, catalog):
    import subprocess
    print("\n🩺 Running Agent Genesis System Healthcheck...\n" + "="*55)
    
    # 1. Python Check
    py_ver = sys.version.split()[0]
    print(f"  🐍 Python Version:       {py_ver} ", end="")
    if sys.version_info >= (3, 10):
        print("[\033[32mOK\033[0m]")
    else:
        print("[\033[33mWarning: Recommended 3.10+\033[0m]")

    # 2. Git Check
    try:
        git_res = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        print(f"  📦 Git Runtime:          {git_res.stdout.strip()} [\033[32mOK\033[0m]")
    except Exception:
        print("  📦 Git Runtime:          Not detected [\033[33mUsing HTTPS Fallback\033[0m]")

    # 3. Vault & Catalog
    print(f"  🧰 Skills Vault:          {len(catalog)} indexed skills [\033[32mOK\033[0m]")

    # 4. Brand Design Systems
    if DESIGN_LIB_DIR.is_dir():
        brand_count = len([d for d in DESIGN_LIB_DIR.iterdir() if d.is_dir()])
        print(f"  🎨 Brand Design Systems: {brand_count} brands available [\033[32mOK\033[0m]")
    else:
        print("  🎨 Brand Design Systems: Not found [\033[31mFAIL\033[0m]")

    # 5. Active Environment Target
    target = get_target_dir(args.target, args.global_install)
    print(f"  🎯 Target Directory:     {target}")
    
    if target.is_dir():
        active = [d.name for d in target.iterdir() if d.is_dir()]
        est_tokens = len(active) * 150
        print(f"  ⚡ Active Skills:        {len(active)} active (~{est_tokens:,} tokens) [\033[32mOK\033[0m]")
        if active:
            print(f"     Active: {', '.join(sorted(active)[:10])}{'...' if len(active) > 10 else ''}")
    else:
        print("  ⚡ Active Skills:        No active skills directory yet [\033[33mRun /setup or profile\033[0m]")

    # 6. Memory Check
    mem_file = Path.cwd() / "memory" / "MEMORY.md"
    if mem_file.is_file():
        print(f"  🧠 Living Memory:        Present at {mem_file.relative_to(Path.cwd())} [\033[32mOK\033[0m]")
    else:
        print("  🧠 Living Memory:        Not initialized in current workspace [\033[33mPending setup\033[0m]")

    print("="*55)
    print("✨ System diagnostic complete! Architected by viklabs.pages.dev\n")

def main():
    parser = argparse.ArgumentParser(description="Skills Manager CLI for Agent Genesis Kit")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # search
    p_search = subparsers.add_parser("search", help="Search skills in the vault")
    p_search.add_argument("query", help="Search keyword")
    p_search.add_argument("--limit", type=int, default=10, help="Max results")

    # list
    subparsers.add_parser("list", help="List skill categories")

    # add
    p_add = subparsers.add_parser("add", help="Add skills from vault to target")
    p_add.add_argument("skills", nargs="+", help="Skill names")
    p_add.add_argument("--target", help="Target skills directory")
    p_add.add_argument("--global", dest="global_install", action="store_true", help="Install globally (~/.gemini/config/skills)")

    # remove
    p_remove = subparsers.add_parser("remove", help="Remove active skills")
    p_remove.add_argument("skills", nargs="+", help="Skill names")
    p_remove.add_argument("--target", help="Target skills directory")
    p_remove.add_argument("--global", dest="global_install", action="store_true", help="Remove from global (~/.gemini/config/skills)")

    # profile
    p_profile = subparsers.add_parser("profile", help="Activate curated token-diet profile")
    p_profile.add_argument("name", help="Profile: gamedev, devops, web, all-in-one, core")
    p_profile.add_argument("--target", help="Target skills directory")
    p_profile.add_argument("--global", dest="global_install", action="store_true", help="Apply globally (~/.gemini/config/skills)")

    # designs
    subparsers.add_parser("list-designs", help="List all 74 brand design systems")
    p_design = subparsers.add_parser("design", help="View or export brand design system")
    p_design.add_argument("brand", help="Brand name (apple, stripe, linear, etc.)")
    p_design.add_argument("--copy-to", help="Destination file path to copy DESIGN.md")

    # sync
    subparsers.add_parser("sync", help="Sync active skills between local and global")

    # doctor
    p_doc = subparsers.add_parser("doctor", help="Run diagnostic healthcheck")
    p_doc.add_argument("--target", help="Target skills directory")
    p_doc.add_argument("--global", dest="global_install", action="store_true", help="Check global directory")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    catalog = load_catalog()

    if args.command == "search":
        cmd_search(args, catalog)
    elif args.command == "list":
        cmd_list(args, catalog)
    elif args.command == "add":
        cmd_add(args, catalog)
    elif args.command == "remove":
        cmd_remove(args, catalog)
    elif args.command == "profile":
        cmd_profile(args, catalog)
    elif args.command == "list-designs":
        cmd_list_designs(args)
    elif args.command == "design":
        cmd_design(args)
    elif args.command == "sync":
        cmd_sync(args, catalog)
    elif args.command == "doctor":
        cmd_doctor(args, catalog)

if __name__ == "__main__":
    main()
