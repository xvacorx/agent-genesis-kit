---
name: game-design-studio
description: Professional game design documentation, vertical slice scoping, art/sound bibles, game loops, economy models, and Unity 6 LTS best practices. Uses standardized AAA templates from tools/game_design_templates and tools/unity_6_reference.
category: gamedev
displayName: Game Design Studio & Unity 6 Reference
license: MIT
compatibility: Markdown, Unity 6 LTS (6000.x)
---

# Game Design Studio & Unity 6 Reference

A professional framework for game design documentation, vertical slice scoping, and Unity 6 LTS best practices. Extracted and distilled from production AAA game studio methodologies.

---

## 📂 Resource Directories

* **Templates Root:** `tools/game_design_templates/` (or `Jarvis/library/game_design/templates/` in Google Drive)
* **Guidance Guides:** `tools/game_design_templates/guidance/`
* **Unity 6 LTS Reference:** `tools/unity_6_reference/` (or `Jarvis/library/game_design/unity_6_reference/`)

---

## 🎯 1. Core Design Templates & When to Use Them

### A. Pre-Production & Pitch
* **`pitch-document.md`**: Executive summary, elevator pitch, target audience, core loop, and unique selling proposition (USP).
* **`game-concept.md`**: Comprehensive creative vision, player fantasy, high-level mechanics, and target emotions.
* **`game-pillars.md`**: 3–4 non-negotiable guiding pillars used as decision filters across all disciplines.

### B. Systems & Mechanics (GDDs)
* **`game-design-document.md`**: Standardized system specification (Core Rules, State Machine Transitions, Edge Cases, Formulas, Telemetry/Analytics).
  * *Guidance:* Read `guidance/game-design-document-guide.md` before authoring complex systems.
* **`difficulty-curve.md`**: Pacing, skill progression, ramp-up phases, and mastery curves.
* **`economy-model.md`**: Faucets, sinks, soft/hard currencies, inflation controls, and upgrade progression.

### C. Visual & Audio Direction
* **`art-bible.md`**: Visual pillars, color palettes, lighting rules, silhouette guidelines, asset pipeline specifications, and "Dos & Don'ts".
* **`sound-bible.md`**: Audio identity, dynamic mix hierarchies, interactive music cues, SFX categorization, and silence usage.

### D. UX & UI Specifications
* **`ux-spec.md`**: User journeys, information hierarchy, input mapping, and navigation state machines.
* **`hud-design.md`**: Screen layout, contextual element visibility, screen safe-areas (mobile notches/cutouts), and alert priorities.
  * *Guidance:* Consult `guidance/hud-design-guide.md` and `guidance/accessibility-requirements-guide.md`.

### E. Vertical Slice & Production Milestones
* **`vertical-slice-report.md`**: Definition of a 3–5 minute representative playable loop proving pipeline velocity, fun factor survival, and tech feasibility.
* **`technical-design-document.md`**: Architecture layers, data structures, network topology, and performance budgets.
* **`prototype-report.md`**: Fast falsifiable validation testing (is this mechanic actually fun?).

---

## ⚡ 2. Unity 6 LTS Reference Guidelines

When implementing gameplay or architectural code in Unity 6 LTS (`6000.x`):

### 1. Modern C# Patterns (Unity 6 / .NET Standard 2.1+)
* Use `record` for immutable telemetry, save data, and network packets:
  ```csharp
  public record PlayerStats(int Health, int Coins, float Speed);
  ```
* Use pattern matching switch expressions instead of cascaded `if-else`:
  ```csharp
  var action = state switch {
      FrogState.Idle => HandleIdle(),
      FrogState.Jumping => HandleJump(),
      FrogState.TongueAttacking => HandleTongue(),
      _ => null
  };
  ```

### 2. Modern Unity APIs (Zero-Deprecation)
* **Finding Objects:** Always use `FindFirstObjectByType<T>()` or `FindAnyObjectByType<T>()`. **Never** use `FindObjectOfType<T>()`.
* **Async Asset Loading:** Use Addressables with `async/await` rather than synchronous `Resources.Load`.
* **Input System:** Use `InputActionReference` with standard C# events rather than `Input.GetKeyDown` or polling.
* **Module-Specific References in `tools/unity_6_reference/`:**
  * `current-best-practices.md`: Verified modern best practices.
  * `breaking-changes.md`: Upgrades from Unity 2022/2023.
  * `deprecated-apis.md`: Exhaustive list of deprecated APIs and their replacements.
  * `modules/animation.md`, `modules/audio.md`, `modules/physics.md`, `modules/rendering.md`, `modules/ui.md`.

---

## 🚀 3. Authoring Workflow Protocol

When Vik or Jarvis needs to document a new mechanic, level, or architecture:
1. Identify the matching template in `tools/game_design_templates/`.
2. Inspect the corresponding guidance doc in `guidance/` if needed.
3. Fill out the specification concisely—avoiding filler text, focusing on:
   - Input/Output contracts
   - State transition tables
   - Precise numeric formulas and curves
   - Memory & performance constraints
4. Save the finalized GDD directly into the relevant project's documentation folder or `Jarvis/library/game_design/`.

