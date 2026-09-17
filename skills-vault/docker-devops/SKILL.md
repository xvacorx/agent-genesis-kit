---
name: docker-devops
description: Containerization, Docker Compose orchestration, and Linux server operations guidelines.
---

# Docker & DevOps Engineering Skill

Guidelines for building lightweight, secure, and production-ready containers.

---

## 🐳 Best Practices

1. **Multi-Stage Builds:**
   - Separate build-time tooling from the final lightweight runtime image (e.g., Alpine or Distroless).
2. **Security & Non-Root Execution:**
   - Never run container payloads as root in production. Define a dedicated non-root user.
3. **Environment & Secrets Hygiene:**
   - Inject secrets via environment variables or Docker secrets.
   - Never bake API keys or sensitive credentials into Dockerfiles.
4. **Reproducible Compose Files:**
   - Use standardized `compose.yaml` files with explicit volume mounts, health checks, and restart policies.
