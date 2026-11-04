# Rule: Code Quality, Master Anti-Slop & STOP & EQUIP Protocol

> [!IMPORTANT]
> **Zero Tolerance for AI Slop & Static Hallucinations:**
> The assistant is prohibited from producing sterile, generic, or low-effort code. Specialized knowledge must be retrieved dynamically from the skills vault rather than hallucinated from static memory.

---

## 🛑 Protocol: STOP & EQUIP (Zero Improvisation from Memory)

1. **Autonomous Tool Equipping:**
   - When a task involves a specialized technical domain (e.g. Tailwind/CSS animations, shaders, pixel art, Kubernetes, Svelte, security auditing, Unity physics, game design documents):
   - **The assistant MUST invoke `equip_skill` via `agent-tools` MCP or CLI before generating code.**
   - Never rely on generic static memory when a curated skill exists in the offline vault.
2. **Transparent Brief Notification:**
   - Inform the user in a single concise line (e.g., *"⚡ Equipped skill `taste-skill` and retrieved `Linear` design tokens for this UI component"*).

---

## 🎨 Master Anti-Slop Design Directives (Craftsmanship Standards)

When generating user interfaces, web applications, or frontends:
1. **Design System Mandatory:**
   - Retrieve real design tokens via `get_brand_design` (e.g. Linear, Stripe, Supabase, Apple, Raycast) or equip `taste-skill` / `antislop-ui`.
2. **Depth & Layered Surfaces:**
   - Deep background tones (`#08090a`, `#0b0f17`, `#0c0a1d`), never flat `#000000` or raw hospital-white `#ffffff`.
   - Subtle radial gradients, dark glassmorphism (`backdrop-blur-md`, `rgba(15, 23, 42, 0.65)`), and delicate borders (`border border-white/[0.08]`).
3. **Micro-Interactions & Tactile Feedback:**
   - Active micro-compression on click (`active:scale-[0.98]`), spring transitions (`cubic-bezier(0.16, 1, 0.3, 1)`), and glow halos on hover.
4. **Editorial Typography:**
   - Tight tracking on headers (`tracking-tight`), monospace numbers/data (`font-mono`), and relaxed body leading (`leading-relaxed`).
5. **Accessibility Contrast Audit:**
   - Always verify text contrast via `check_contrast` ensuring WCAG AA >= 4.5:1 (normal text) and >= 3.0:1 (large text).

---

## 🛡️ Non-Destructive Integrity
1. **Never delete or blindly overwrite existing working code.**
2. **Maintain backward compatibility and clean modular abstractions.**
