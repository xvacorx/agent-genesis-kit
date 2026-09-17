---
name: skills-vault-manager
description: "Query, search, inspect, and activate skills from the offline Skills Vault (880+ curated skills) in AntigravityExtras on-demand without bloating token context."
category: meta
displayName: Skills Vault Manager
---

# Skills Vault Manager

You have an offline vault containing **880+ specialized skills** located at `c:\AntigravityExtras\skills-vault/` and managed via `c:\AntigravityExtras\skills_manager.py`.

## When to use this skill:
- When a task involves a specialized framework, tool, cloud provider, or workflow not present in currently active skills (e.g. Terraform, Kubernetes, GraphQL, Svelte, Rust, Go, Next.js, AWS, Azure, Ansible, Blender, etc.).
- When the user asks to search, list, or activate new skills.

## Commands:

### 1. Search the Skills Vault:
```bash
python c:\AntigravityExtras\skills_manager.py search <keyword>
# Example:
python c:\AntigravityExtras\skills_manager.py search kubernetes
```

### 2. View Skill details & instructions:
```bash
python c:\AntigravityExtras\skills_manager.py show <skill-name>
# Example:
python c:\AntigravityExtras\skills_manager.py show kubernetes-expert
```

### 3. Activate/Install a Skill:
- **Into Current Workspace (`Jarvis`):**
  ```bash
  python c:\AntigravityExtras\skills_manager.py install <skill-name>
  ```
- **Globally (`~/.gemini/config/skills`):**
  ```bash
  python c:\AntigravityExtras\skills_manager.py install <skill-name> --global
  ```

### 4. Install a Curated Bundle:
```bash
python c:\AntigravityExtras\skills_manager.py install-bundle <bundle-name>
# Available bundles: proxmox-devops, unity-gamedev, fullstack-web, security-audit, essential-jarvis
```

### 5. Check Installed Skills:
```bash
python c:\AntigravityExtras\skills_manager.py installed
```
