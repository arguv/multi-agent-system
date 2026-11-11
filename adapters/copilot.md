# GitHub Copilot adapter

Load AGENTS.md, workflow.md, and the assigned role pair as context. Where repository instructions are required, use a thin .github/copilot-instructions.md entry referencing the canonical files. Verify discovery in the installed client.

Canonical entry: `../AGENTS.md`; workflow: `../workflow.md`; roles: `../agents/`.
Read the active role's instructions and skills before acting, announce the stack, and preserve both user lifecycle gates. Adapter configuration must not change the core workflow. If context loading is unavailable, report the limitation rather than claiming the role files were read.

No automatic discovery compatibility is guaranteed by this note. Verify the installed runner's behavior. Keep executable invocation syntax and runner-specific settings outside the canonical core.

Output contract: the actual project is built in `../work/`; every plan, report, review, test result, and member summary is written to `../description/`. Resolve these paths from this adapter's directory. Both output folders stay empty before a user project starts; do not seed them during runner setup or framework maintenance. Preserve project and reports during cleanup.
