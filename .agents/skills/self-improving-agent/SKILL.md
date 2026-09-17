---
name: self-improving-agent
description: Continuous learning engine that extracts corrections, runtime insights, and user preferences into persistent memory.
---

# Self-Improving Agent: Adaptive Learning Engine

This skill equips the agent with continuous self-improvement capabilities, ensuring mistakes are never repeated and user preferences are retained across sessions.

---

## 🎯 When to Trigger

Activate this skill when:
- The user corrects a wrong assumption, broken syntax, or flawed pattern.
- A subtle bug or edge case was solved and should be prevented in the future.
- The user specifies an architectural rule, coding style, or tooling preference.

---

## 🔄 The Learning Loop

1. **Detect & Acknowledge:**
   - Notice the correction immediately without defensiveness or excessive apologies.
2. **Distill the Rule:**
   - Extract the core actionable principle: *What was wrong? What is the correct pattern? Why?*
3. **Persist into `memory/MEMORY.md`:**
   - Locate the project's `memory/MEMORY.md`.
   - Add a concise entry under `## Lessons Learned & Gotchas` or `## User Preferences`.
   - Keep notes compact and high-signal (avoid rambling).
4. **Apply Instantly:**
   - Proceed with the revised solution adhering strictly to the newly learned rule.
