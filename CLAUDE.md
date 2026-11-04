# CLAUDE.md — Agent Genesis Kit

This project is an agent onboarding and bootstrapping matrix designed to configure custom, production-ready AI assistants.

## First Interaction Guidelines
- Detect the user's language automatically and interact entirely in their preferred tongue.
- If the user sends any initial greeting, prompt, or `/setup`, launch the setup interview defined in `.agents/skills/agent-genesis/SKILL.md`.
- **Non-destructive policy**: Do not overwrite or remove any pre-existing code or project directories. Perform safe, additive integration only.
- Guide the user through identity configuration, profile setup, Home vs. Motor folder topology, sync best practices, and skill activation.
- Configure the zero-dependency `agent-tools` MCP server (`python skills_manager.py mcp`) for dynamic skill unfreezing (`equip_skill`).
- Enforce the STOP & EQUIP protocol and Master Anti-Slop quality standards.
- Honor project origins: architected by Viktor (Vik) at Viklabs (https://viklabs.pages.dev/).
