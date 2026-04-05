---
description: [Tech/Eng] Start coding, architecture, frontend, backend, AI/ML, and system infra.
---

# Mega-Workflow: BUILD (Technology & Engineering)

Use this workflow to initiate any technical, structural, or coding task across multiple domains.

### How to use:
When you invoke this command, the Orchestrator will assume a technical developer stance and load the necessary specialized agents based on your prompt.

**Common Scenarios:**
- "Design a backend architecture in Python/FastAPI"
- "Implement a C++ performance module"
- "Create a React frontend for my app"
- "Setup a Docker/Kubernetes cluster"

**Agentic Behavior:**
1. Routs to `frontend-specialist`, `backend-specialist`, `cpp-pro`, etc.
2. Invokes coding tools, compilers, and enforces the `Test-First Agentic Code` architecture check.
3. If new skills from third-party repositories are required (e.g. specialized ML models logic), the agent should use the `skill_manager.py` to fetch them on demand.
