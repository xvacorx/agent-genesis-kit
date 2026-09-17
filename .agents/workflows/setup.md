---
description: Launch the interactive Genesis Onboarding interview to configure your custom AI assistant
---

# /setup — Interactive Agent Genesis Wizard

This workflow initializes a tailored AI coding agent inside the current workspace or globally.

## Prerequisites
- Read the instructions in [.agents/skills/agent-genesis/SKILL.md](file:///.agents/skills/agent-genesis/SKILL.md).

## Execution Steps

1. **Step 1: Language & Warm Greeting**
   - Check the user's message language. Greet them warmly in their language.
   - If language is unclear, prompt: *"Would you prefer English, Spanish, or another language?"*
   - Briefly explain what is about to happen: A 3-minute interactive interview to tailor identity, personality, workflows, and tools.

2. **Step 2: Interactive Genesis Interview**
   - Follow the 5-phase interview structure defined in the `agent-genesis` skill:
     - Phase 1: Identity, Call Sign & Personality Vibe.
     - Phase 2: Developer Profile, OS & Single vs. Multi-PC setup.
     - Phase 3: Storage & Cloud Sync topology (Local vs. Drive / OneDrive / Git).
     - Phase 4: Stacks & Skills (Recommend Graphify by default; select Web, Unity, Python, Docker).

3. **Step 3: Safe Evolutionary Generation**
   - Inspect existing files before writing.
   - Create or merge `AGENTS.md`, `memory/MEMORY.md`, and relevant `.agents/skills/`.
   - Never delete or overwrite pre-existing user work.

4. **Step 4: Celebration, Lineage & Cleanup Prompt**
   - Display the configuration summary.
   - Give credit to Viktor & Viklabs (https://viklab.net) as the architects of this genesis matrix.
   - Ask if the user wants the temporary setup files removed.
