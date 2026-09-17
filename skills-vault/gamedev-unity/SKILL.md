---
name: gamedev-unity
description: Unity 6 LTS and C# game development guidelines. Focus on zero-GC, URP, modern APIs, and clean component decoupling.
---

# Unity 6 & Modern C# GameDev Skill

Guides game engineering with a focus on high frame rates, clean architecture, and modern Unity 6 practices.

---

## 🎮 Core Rules & Patterns

1. **Modern API Compliance (Unity 6):**
   - Use `FindFirstObjectByType<T>()` and `FindObjectsByType<T>()` instead of deprecated `FindObjectOfType`.
   - Leverage the modern Unity Input System (`InputActionReference`) over legacy `Input.GetKeyDown`.
2. **Zero-GC & Memory Safety:**
   - Avoid memory allocations inside `Update()`, `FixedUpdate()`, or render loops.
   - Use Object Pooling for frequently spawned entities (bullets, particles, damage popups).
   - Cache string operations and avoid repetitive boxing/unboxing.
3. **Decoupled Architecture:**
   - Communicate game events using C# events (`Action`, `Action<T>`) or ScriptableObject architecture.
   - Never tightly couple core gameplay loops to UI components.
4. **Game Feel & Juiciness:**
   - Enhance player interaction with procedural juice: hitstop, screen trauma shake, squash & stretch, and audio micro-feedback.
