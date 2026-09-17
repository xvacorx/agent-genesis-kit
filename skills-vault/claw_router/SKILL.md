---
name: claw_router
description: Smart LLM routing integration guidelines.
---

# ClawRouter Integration

ClawRouter routes LLM requests to the cheapest capable model across providers like OpenAI, Anthropic, Google, and DeepSeek, saving up to 67% on inference costs.

## Classification Tiers
- **SIMPLE:** Factual lookups, greetings, translations -> Gemini Flash (Rule-based routing)
- **MEDIUM:** Summaries, explanations, data extraction -> DeepSeek Chat
- **COMPLEX:** Code generation, deep analysis -> Claude Sonnet / GPT-4o
- **REASONING:** Math, proofs, logic -> OpenAI o-series

In the context of managing the local OpenClaw gateway, check and modify the model configuration in `backup_openclaw/openclaw.json` or native configuration to use `blockrun/auto` for smart cost-effective routing.
