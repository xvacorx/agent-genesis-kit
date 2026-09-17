---
name: systematic-debugging
description: Root-cause debugging protocol. Formulate hypotheses, verify evidence, and diagnose before changing code.
---

# Systematic Debugging Protocol

Avoid "guess-and-check" bug fixing. Always isolate the root cause methodically before introducing changes.

---

## 🔬 The 4-Phase Protocol

### Phase 1: Reproduce & Collect Evidence
- Read the exact error trace, exception message, or unexpected output.
- Identify the exact inputs and conditions that trigger the defect.
- Do not modify code yet.

### Phase 2: Formulate Hypotheses
- State explicitly what might be failing and why based on evidence:
  - *Is it a null reference / undefined variable?*
  - *Is it an asynchronous race condition or stale state?*
  - *Is it an environment / dependency / path mismatch?*

### Phase 3: Minimal Verification
- Inspect the relevant code lines, log outputs, or run a diagnostic command.
- Confirm or invalidate the hypothesis before applying any edit.

### Phase 4: Root Cause Resolution
- Implement the cleanest fix addressing the underlying mechanism, not just silencing symptoms.
- Validate that the fix resolves the defect without introducing side effects or regressions.
