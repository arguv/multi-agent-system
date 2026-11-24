# DeepSeek and other runners adapter

Provide AGENTS.md, workflow.md, the assigned role file, and the active stack file through the runner’s file/context mechanism. Do not assume native role delegation or skill discovery; use explicit sequential role passes if needed.

Canonical entry: `../AGENTS.md`; workflow: `../workflow.md`; roles: `../agents/`.
Read the active role's file and `../stacks/<Active stack>.md` (named by the `Active stack:` line in `../workflow.md`) before acting, announce the stack, and preserve both user lifecycle gates. Adapter configuration must not change the core workflow. If context loading is unavailable, report the limitation rather than claiming the role files were read.

No automatic discovery compatibility is guaranteed by this note. Verify the installed runner's behavior. Keep executable invocation syntax and runner-specific settings outside the canonical core.

Output contract: the actual project is built in `../work/`; every plan, report, review, test result, and member summary is written to `../description/` as numbered reports (`01_requirements.md` to `09_manual_qa_report.md`). Resolve these paths from this adapter's directory. Both output folders stay empty before a user project starts; do not seed them during runner setup or framework maintenance. Cleanup happens only on the user command `finish work`, which empties both folders.
