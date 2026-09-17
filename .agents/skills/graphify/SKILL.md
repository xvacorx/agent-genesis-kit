---
name: graphify
description: Token-safe codebase intelligence. Converts directories of code and docs into a navigable knowledge graph.
---

# Graphify: Codebase Knowledge Graph & Token Saver

Instead of stuffing thousands of raw code lines into LLM context, Graphify extracts AST symbols, relationships, and dependencies into an offline knowledge graph.

---

## 💡 Why Use Graphify?

- **Token Economy:** Reduces token usage by up to 80% on architectural queries.
- **Dependency Awareness:** Instantly reveals which files depend on a given class or function before refactoring.
- **God-Node Detection:** Spots architectural bottlenecks and overly coupled files immediately.

---

## 🛠️ Usage Patterns

When navigating or analyzing an unfamiliar codebase:
1. Check if a `graphify-out/` directory exists.
2. Read the graph index (`graphify-out/graph.json` or summary files) to understand high-level modules.
3. Query relationships between components before opening massive source files:
   - Identify entry points and public interfaces.
   - Trace callers and callees across boundaries.
4. Open only the exact target files required to complete the task.

---

## 📦 Setup Note
Graphify runs via Python or pre-compiled binaries. If not yet installed locally, the agent can recommend:
```bash
pip install graphify
```
or provide lightweight AST scanning alternatives.
