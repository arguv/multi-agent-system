# Universal Software Delivery Team

Before any work, read `agents/orchestrator/instructions.md` and `agents/orchestrator/SKILL.md` when coordinating. Every acting member must read its own pair before doing its work.

Canonical workflow, lifecycle gates, and artifact contracts: `workflow.md`.
A new task begins in requirements collection; do not orchestrate until the user sends `work start`.
Do not declare completion or clean working files until the user sends `work done` after reviewing delivery.

| Role | Instructions | Skills |
| --- | --- | --- |
| Agent Orchestrator | `agents/orchestrator/instructions.md` | `agents/orchestrator/SKILL.md` |
| Senior Architect | `agents/architect/instructions.md` | `agents/architect/SKILL.md` |
| DevOps Engineer | `agents/devops/instructions.md` | `agents/devops/SKILL.md` |
| Senior Software Engineer | `agents/engineer/instructions.md` | `agents/engineer/SKILL.md` |
| Senior Test Engineer | `agents/test-engineer/instructions.md` | `agents/test-engineer/SKILL.md` |
| Senior Code Reviewer | `agents/reviewer/instructions.md` | `agents/reviewer/SKILL.md` |
| Senior QA Automation Engineer | `agents/qa-automation/instructions.md` | `agents/qa-automation/SKILL.md` |
| Senior Manual QA Engineer | `agents/qa-manual/instructions.md` | `agents/qa-manual/SKILL.md` |

Use the same canonical files for every runner and stack. Tool-specific loading notes belong only in `adapters/`. If the runner cannot create agents, perform separate role passes with explicit handoffs and the same gates. Never imply independent review occurred when one runner performed it.

## Output folders
`work/` contains the actual user project, including source, tests, and scaffolding. `description/` contains all task plans, agent reports, review/test/QA results, and final summaries. Both folders stay empty before a user project starts. Team-framework maintenance does not generate project reports. Never restore deleted sample or framework-build results. Cleanup preserves the project and reports.

Before work start, discuss requirements in chat. After work start, create the task report and needed subdirectories on demand. Missing future-stage reports are normal; never fabricate completion evidence.
