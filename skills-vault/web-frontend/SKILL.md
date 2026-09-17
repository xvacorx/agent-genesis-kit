---
name: web-frontend
description: Senior frontend architecture for modern React, Tailwind CSS, TypeScript, and responsive design systems.
---

# Web & Frontend Engineering Skill

Guides the creation of sleek, responsive, and performant web applications adhering to modern UX standards.

---

## 🎨 Architectural Standards

1. **Semantic Design Tokens:**
   - Use CSS custom properties or theme configuration for colors, spacing, and typography.
   - Avoid hardcoding magic hex values across components.
2. **State & Separation of Concerns:**
   - Keep presentational components clean and focused.
   - Decouple business logic into custom hooks or state stores (Zustand, Context).
3. **Performance & Bundle Size:**
   - Implement lazy loading (`React.lazy` / dynamic imports) for non-critical views and modals.
   - Optimize images and avoid rendering heavy layouts inside animation loops.
4. **Accessibility (a11y):**
   - Ensure proper heading hierarchy (`<h1>` to `<h6>`).
   - Use interactive elements with accessible labels (`aria-label`) and keyboard focus outlines.
