# DeepSeek and other runners adapter

Provide AGENTS.md, workflow.md, and the assigned role pair through the runner’s file/context mechanism. Do not assume native role delegation or skill discovery; use explicit sequential role passes if needed.

Canonical entry: `../AGENTS.md`; workflow: `../workflow.md`; roles: `../agents/`.
Read the active role's instructions and skills before acting, announce the stack, and preserve both user lifecycle gates. Adapter configuration must not change the core workflow. If context loading is unavailable, report the limitation rather than claiming the role files were read.

No automatic discovery compatibility is guaranteed by this note. Verify the installed runner's behavior. Keep executable invocation syntax and runner-specific settings outside the canonical core.
