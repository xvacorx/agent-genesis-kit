---
name: python-automation
description: Clean Python architecture for automation scripts, CLI utilities, and robust data pipelines.
---

# Python Automation & Scripting Skill

Engineering guidelines for creating robust, maintainable, and type-hinted Python tools.

---

## 🐍 Standards & Patterns

1. **Virtual Environments First:**
   - Always operate inside a dedicated virtual environment (`.venv`).
   - Pin requirements in `requirements.txt` or `pyproject.toml`.
2. **Type Hints & Static Analysis:**
   - Use Python 3.10+ typing annotations (`list[str]`, `str | None`, `Callable`).
   - Keep functions pure and side-effect free where possible.
3. **CLI Design:**
   - Use `argparse`, `typer`, or `click` for command-line tools.
   - Implement clear `--help` descriptions and graceful error exits (`sys.exit(1)`).
4. **Resilient File & Network Operations:**
   - Use `pathlib.Path` over raw string path manipulation.
   - Use contextual managers (`with open(...)`) to guarantee resource cleanup.
