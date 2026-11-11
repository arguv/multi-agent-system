# Universal Multi-Agent Software Delivery Team

A portable Markdown team for feature work, bug fixes, and new projects. Eight senior roles share one workflow across PHP, Python, Go, and JavaScript/TypeScript. No runner-specific syntax is needed in the canonical definitions.

## Start a task
1. Load `AGENTS.md` and `workflow.md`, then read the Orchestrator's two files in `agents/orchestrator/`.
2. Describe the task, target repository, acceptance criteria, constraints, and stack. The Orchestrator collects requirements first.
3. Send `work start` to begin the gated workflow.
4. Review the delivered changes, evidence, and eight summaries in `description/`.
5. Send `work done` to accept delivery and authorize safe cleanup.

Architecture → environment → implementation with code-level tests → review → automated QA → manual QA when required → delivery → user acceptance → cleanup. Failed stages return to the responsible member and repeat; downstream evidence is renewed after changes.

Each member reads its own `instructions.md` and `SKILL.md` before working. Instructions remain stack-independent. Skills contain shared capabilities and selectable PHP, Python, Go, and JS/TS sections. Unselected stacks remain readable and inactive, allowing a switch without edits.

See `workflow.md` for artifact paths, gates, stage criteria, cleanup, and delivery into another repository. The actual user project lives in `work/`. Every report, plan, review, test result, and member summary lives in `description/`. Both folders are empty before a user project starts. Cleanup preserves the project and reports.

## Loading into a runner
Use the thin notes in `adapters/`. Automatic discovery varies by runner and installation; explicit loading of the canonical role pair is always the fallback. A single runner can perform separate role passes with recorded handoffs; it must disclose that review was not independent.

## Validate this framework
Run `python3 scripts/validate.py` from the repository root. It checks role metadata, instruction length, stack coverage, workflow artifacts, and local Markdown references. This is a structural check, not proof that an external runner automatically discovers these files.
