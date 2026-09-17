---
name: image_gen
description: Generate images via BlockRun's image API or native generate_image tool. Trigger when the user asks to generate, create, draw, or make an image/asset.
---

# Image Generation Skill

When the user asks to generate, create, draw, or make an image/asset:
1. First, check if you can use the native `generate_image` tool directly to generate user interfaces, icons, or design assets.
2. Alternatively, if specifically requested or in the context of the OpenClaw gateway, call the BlockRun image API:
   * **Endpoint:** POST to `http://localhost:8402/v1/images/generations`
   * **Payload:**
     ```json
     {
       "model": "google/nano-banana",
       "prompt": "<user's prompt>",
       "size": "1024x1024",
       "n": 1
     }
     ```
   * **Models:** `google/nano-banana` (default), `google/nano-banana-pro` (high-res), `openai/dall-e-3` (photorealistic).
   * Display the result: `![generated image](url_returned_in_response)`
