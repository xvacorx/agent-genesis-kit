---
name: antislop
description: Strict quality filter preventing generic boilerplate, placeholders, deprecated APIs, and AI-generated slop.
---

# Anti-Slop: High-Fidelity Engineering Standard

AI code generation often defaults to generic, bloated, or lazy patterns. This standard enforces production-grade rigor.

---

## 🚫 Zero-Tolerance Rules

1. **No Lazy Placeholders:**
   - Never write `// TODO: implement logic here`, `/* add styles here */`, or `... rest of code`.
   - Deliver complete, functional, drop-in solutions.
2. **No Deprecated Patterns:**
   - Use current runtime and language standards (e.g., modern C# pattern matching, React hooks/functional components, modern async/await).
3. **No Unnecessary Abstractions:**
   - Do not create 5 layers of premature factory classes for a 10-line feature. Keep solutions direct, clean, and idiomatic.
4. **No Hallucinated Dependencies:**
   - Never import external packages without verifying they exist or checking `package.json` / `requirements.txt` / project manifests first.
5. **No Blind Overwrites:**
   - Retain existing code comments, docstrings, and unrelated functionality intact when refactoring.
