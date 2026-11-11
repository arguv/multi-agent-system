# OpenAI Codex adapter

Use the root AGENTS.md as the repository discovery entry. It assigns the coordinating chat to the Orchestrator and instructs it to read its role pair and workflow automatically. Users only need to describe their project, then send work start after requirements collection. Nested role files are loaded by the agent following the root instructions; they are not assumed to load automatically. Explicit worker assignments override the default Orchestrator role.

Canonical entry: `../AGENTS.md`; workflow: `../workflow.md`; roles: `../agents/`.
Read the active role's instructions and skills before acting, announce the stack, and preserve both user lifecycle gates. Adapter configuration must not change the core workflow. If context loading is unavailable, report the limitation rather than claiming the role files were read.

No automatic discovery compatibility is guaranteed by this note. Verify the installed runner's behavior. Keep executable invocation syntax and runner-specific settings outside the canonical core.

Output contract: the actual project is built in `../work/`; every plan, report, review, test result, and member summary is written to `../description/`. Resolve these paths from this adapter's directory. Both output folders stay empty before a user project starts; do not seed them during runner setup or framework maintenance. Preserve project and reports during cleanup.
