# Universal Multi-Agent Software Delivery Team

A portable, tool-agnostic Markdown framework that turns any AI engine (Claude, DeepSeek, Copilot, Cursor, Codex, or a local LLM) into a virtual IT department. It takes a project from the first idea to delivery and testing. If the AI can read files and write code, it can run this team.

## Core concept: one chat, eight hats
A hub-and-spoke model inside a single chat. The Orchestrator collects requirements, plans the work, and delegates to specialists (or sequentially "puts on the hat" of each one when the runner has no delegation). Memory lives in files, not chat history: agents pass information by reading and writing the numbered reports in `description/`.

## The team
| Role | File |
| --- | --- |
| Agent Orchestrator (main agent and planner) | `agents/orchestrator.md` |
| Senior Architect | `agents/architect.md` |
| DevOps Engineer | `agents/devops.md` |
| Senior Software Engineer | `agents/engineer.md` |
| Senior Test Engineer | `agents/test-engineer.md` |
| Senior Code Reviewer | `agents/reviewer.md` |
| Senior QA Automation Engineer | `agents/qa-automation.md` |
| Senior Manual QA Engineer | `agents/qa-manual.md` |

## Workflow (user-controlled state machine)
1. **Clarification, no files written.** Open this repository in your runner and describe the task. The root `AGENTS.md` makes the chat the Orchestrator, which asks questions until requirements are clear. Then it waits for you to send exactly `start work`.
2. **Execution, triggered by `start work`.** The Orchestrator writes `01_requirements.md` and `02_project_plan.md`, then Architect and DevOps design the system and prepare the environment, the Engineer writes code into `work/`, and the Reviewer, Test Engineer, QA Automation, and Manual QA check it. Any FAIL goes back to the owner (usually the Engineer) and repeats until all checks PASS.
3. **Cleanup, triggered by `finish work`.** Review the code and reports first. When you send exactly `finish work`, both `work/` and `description/` are emptied immediately, ready for the next project. Copy or commit anything you want to keep beforehand.

## Folders
- `AGENTS.md`: master rulebook (states, token rules, workflow loop).
- `workflow.md`: lifecycle gates, stage criteria, artifact contracts, and the `Active stack:` line.
- `agents/`: eight flat role files, one per role.
- `stacks/`: `php.md`, `python.md`, `go.md`, `js-ts.md` with language-specific rules (frameworks, linting, testing tools).
- `adapters/`: thin loading notes per runner.
- `description/`: the project's "brain", numbered reports `01_requirements.md` through `09_manual_qa_report.md`. Created on demand.
- `work/`: the actual project; the Engineer writes source and tests here. Created on demand.

Both output folders are empty before a project starts and after `finish work`. They may be absent after a fresh checkout because Git does not track empty directories.

## Changing the programming language
The first line of `workflow.md` is:

```
Active stack: php
```

To switch the whole team to another language, change only that value to `python`, `go`, or `js-ts`. Every role file starts by reading `stacks/<Active stack>.md`, so no role file needs editing. To add another language, create `stacks/<name>.md` with the same sections as the existing stack files and set `Active stack: <name>`. Run `python3 scripts/validate.py` afterwards; it checks that the line points to an existing stack file.

## Token efficiency
- No echoing: agents write files and say only "Report saved to `description/05_engineer_report.md`."
- Read only what you need: each role reads its own file, the active stack file, the workflow, and its listed inputs.
- Strict handoff format: `[Role] finished. Report saved to [path]. Handing off to [Next Role].`

## Numbered reports
| File | Written by |
| --- | --- |
| `01_requirements.md`, `02_project_plan.md` | Orchestrator |
| `03_architecture_plan.md` | Architect |
| `04_environment.md` | DevOps |
| `05_engineer_report.md` | Engineer |
| `06_test_report.md` | Test Engineer |
| `07_review_report.md` | Reviewer |
| `08_qa_automation_report.md` | QA Automation |
| `09_manual_qa_report.md` | Manual QA |

Files are created on demand when their stage runs; missing later reports are normal and never fabricated. Optional generated evidence (coverage, logs) goes in `description/evidence/`.

## Loading into a runner
Use the thin notes in `adapters/`. The default Orchestrator entry depends on the runner loading the root `AGENTS.md`. Opening a folder alone does not execute a task; send your project description in chat. A single runner can perform separate role passes with recorded handoffs; it must disclose that review was not independent.

## Validate this framework
Run `python3 scripts/validate.py` from the repository root, and `python3 -m unittest discover -s scripts` for its tests. The validator checks the eight role files, the `stacks/` files and the `Active stack:` line, the `start work` and `finish work` commands, the numbered report paths, local references, and the output-folder contract. It is a structural check, not proof that an external runner discovers these files.
