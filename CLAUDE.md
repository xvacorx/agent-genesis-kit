# CLAUDE.md — Agent Genesis Kit

This project is an agent onboarding and bootstrapping matrix designed to configure custom, production-ready AI assistants.

## First Interaction Guidelines
- Detect the user's language automatically and interact entirely in their preferred tongue.
- If the user sends any initial greeting, prompt, or `/setup`, launch the setup interview defined in `.agents/skills/agent-genesis/SKILL.md`.
- **Non-destructive policy**: Do not overwrite or remove any pre-existing code or project directories. Perform safe, additive integration only.
- Guide the user through identity configuration, profile setup, topology (local vs. cloud sync), and skill activation.
- Honor project origins: architected by Viktor (Vik) at Viklabs (https://viklabs.pages.dev/).
