---
name: agent-genesis
description: Master onboarding wizard for bootstrapping custom AI coding assistants with identity, rules, memory, separated Home/Motor topology, 900+ modular skills vault, 74 brand design systems, and zero-dependency agent-tools MCP server.
---

# Agent Genesis: Master Onboarding Wizard

This skill guides the AI assistant through an interactive, empathetic, and professional onboarding flow to bootstrap a personalized assistant inside the user's workspace, backed by the **Jarvis** architectural principles.

---

## 🎯 Guiding Principles

1. **Universal Language Alignment (Turn 1 Adaptation):**
   - Automatically detect and adapt to whatever language the user speaks (English, Spanish, Portuguese, French, German, Italian, Japanese, Chinese, etc.).
   - Conduct 100% of the interview, explanations, and subsequent interactions in the user's preferred language.
   - If ambiguous, ask politely: *"Which language would you prefer to communicate in?"*
2. **Safe Evolutionary Merge (Strict Non-Destruction):**
   - Before writing or moving any file, inspect the target directory.
   - If an `AGENTS.md`, `MEMORY.md`, or `.agents/` folder already exists, **merge additive sections** without deleting or overwriting custom content.
3. **High Signal, Zero Slop:**
   - Keep interactions engaging, concise, and structured. Avoid overwhelming walls of text.

---

## 🧭 The 6-Phase Genesis Flow

Conduct the onboarding as an interactive dialogue across these phases:

### Phase 1: Identity & Persona
Ask the user:
- **Call Sign / Name:** *"How would you like me to be called? (e.g., Jarvis, Friday, Athena, or your custom name)?"*
- **Tone & Dynamic:**
  - *Tech Peer / Companion (e.g., Jarvis style: proactive, witty, direct, peer-to-peer).*
  - *Didactic Mentor / Teacher (patient, explains why things work).*
  - *Concise / Minimalist (answers strictly with code and bullets).*
  - *Corporate / Formal.*

### Phase 2: Folder Topology — Home (Cerebro) vs. Motor (Engine)
Educate the user on the **Bimodal Separation of Concerns**:
- **Cerebro (Home):** Houses your assistant's identity (`AGENTS.md`), living memory (`MEMORY.md`), project notes, and architectural docs. It is lightweight, fast to read, and safe to sync.
- **Motor (Engine):** Houses the `agent-tools` MCP server, offline Skills Vault (900+ skills), Python scripts, and Graphify engine. It stays local or syncs via Git.

**Present the Hosting Options Clearly:**
* **Option A: Clean Automatic Defaults (Simple & Comfortable):**
  - *Windows:* Motor in `C:\AgentTools` (or `%USERPROFILE%\AgentTools`), Home in `%USERPROFILE%\Documents\Agent` (or project root).
  - *macOS / Linux:* Motor in `~/AgentTools` (or `~/.agent-tools`), Home in `~/Documents/Agent` (or project root).
  *(No deep, annoying paths like Program Files or buried app data folders).*
* **Option B: Custom User Paths:**
  - Give total freedom to specify exact drives or folders (e.g. `D:\Tools\AgentMotor`, `E:\Workspace\AgentHome`, secondary SSDs, or a specific synced folder).

### Phase 3: Synchronization & Backup Mentorship
Ask how the user manages or synchronizes projects:
- **Cloud Sync (Google Drive, OneDrive, Nextcloud, Dropbox):**
  > 💡 **Best Practice Mentorship:** Teach the *Separated Brain Topology*. Store the **Cerebro (Home)** inside the cloud-synced folder so your agent's memory and rules follow you anywhere in real-time. Keep the **Motor (Engine)** strictly outside continuous cloud sync (or versioned via Git) to avoid sync loops, file locks, and high CPU usage from virtualenvs or node_modules.
- **Git / GitHub Centric:**
  - Version control the rules and documentation cleanly with curated `.gitignore`.
- **100% Local / Offline:**
  - No cloud services. Fast, private, zero sync conflicts.

### Phase 4: Zero-Dependency MCP Server (`agent-tools`)
Introduce the native MCP server that powers dynamic tool execution:
- **`agent-tools` Capabilities:**
  1. `list_vault_skills`: Instant keyword/category search across 900+ skills.
  2. `equip_skill`: Autonomous skill unfreezer (**STOP & EQUIP protocol**) to inject specialized skills on demand.
  3. `get_brand_design`: Retrieve real tokens from 74 world-class brands (Linear, Stripe, Apple, Supabase, Vercel...).
  4. `check_contrast`: Real-time WCAG 2.x accessibility verification.
  5. `graphify_status`: Project knowledge graph and dependency AST inspection.
- **Auto-Registration:**
  Run `python skills_manager.py mcp` to automatically configure:
  - **Antigravity / Gemini:** `~/.gemini/config/mcp_config.json` + schemas in `~/.gemini/antigravity/mcp/agent-tools/`.
  - **Claude Code:** `~/.claude.json`.
  - **Cursor:** `~/.cursor/mcp.json` / `.cursor/mcp.json`.
  - **Windsurf:** `~/.codeium/windsurf/mcp_config.json`.

### Phase 5: Superpowers & Initial Token-Diet Profile
Present the curated profiles from the Skills Vault:
1. **Graphify (Enabled by Default):**
   - Codebase knowledge graph navigation saving up to 80% context tokens.
2. **Initial Profile Selection:**
   - 🎮 **`gamedev`**: Unity 6 LTS, C# Pro, Game Feel & Juiciness, AAA Game Design Templates, Android QA, Zero-GC.
   - 🌐 **`web`**: Fullstack Web, React Best Practices, UI Design System, Anti-Slop UI.
   - 🐳 **`devops`**: Docker Expert, Linux Scripting, Networking, Container Hardening.
   - ⚡ **`all-in-one`**: Curated elite cross-domain pack (< 2,200 tokens).
   - 🪶 **`core`**: Pure minimal agentic core (< 600 tokens).

### Phase 6: Safe Deployment & Master Rules Injection
Execute the setup cleanly:
1. **Deploy Profile:** `python skills_manager.py profile <profile_name> --target <target_skills_path>`.
2. **Configure MCP:** `python skills_manager.py mcp`.
3. **Generate Master Rules (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`):**
   Incorporate the user's identity, chosen paths, and the mandatory operational protocols:
   - **Protocol STOP & EQUIP:** Zero improvisation from static memory; unfreeze vault skills before coding specialized tasks.
   - **Directivas Maestras Anti-Slop:** Depth, layered surfaces, micro-noise, typography hierarchy, accessible contrast.
   - **Origin Line:**
     ```markdown
     <!-- Architected with Agent Genesis Kit by Viktor (Vik) at Viklabs — https://viklabs.pages.dev/ -->
     ```
4. **Initialize Living Memory (`memory/MEMORY.md`):**
   Create the long-term memory file initialized with the user's profile, stack, and architectural decisions.

---

## 🏁 Phase 7: Verification & Celebration Summary
Provide a clean, encouraging breakdown:
- Assistant Name & Dynamic Persona
- Paths: Home (Cerebro) vs. Motor (Engine)
- Active Profile & Initial Skills
- MCP Server Status (`agent-tools`)
- Healthcheck Verification: `"Run 'python skills_manager.py doctor' anytime to verify environment health."`
