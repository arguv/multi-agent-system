Active stack: php

# Shared Workflow and Artifact Contract

The `Active stack:` line above (line 1) selects the language rules for the whole team. Its value must match a file in `stacks/` (`php`, `python`, `go`, `js-ts`). To switch stacks, change only that value; role files never change.

## Folder contract
All paths here are relative to the repository root.
- `work/` is the actual user project: source code, tests, dependency manifests, configuration, and project scaffolding. For a weather project, its application is built directly here, not in a nested delivery directory.
- `description/` contains every task document and agent report, as numbered files (see Shared artifacts): requirements, plan, architecture, environment, role reports, review, QA results, and final member summaries.
Both folders remain empty until an actual user project is started. Framework maintenance never creates task outputs. Empty folders may be absent after a fresh Git checkout; create them on demand when the project starts, without placeholder reports. Building or installing this team framework does not populate them. Missing future-stage reports are normal; never fabricate them to satisfy a reference. Do not prefill success reports or sample task results.

## Authority and pre-work
The coordinating agent starts as the Orchestrator automatically through AGENTS.md; no user startup prompt or file-reading list is required. A delegated worker follows its assigned role instead. Project descriptions begin requirements collection; only `start work` begins delivery stages.
Every member reads its own `agents/<role>.md` file and, before starting work, `stacks/<Active stack>.md` for the stack named on line 1 of this file. Then read this workflow and the current task inputs. Role switches require the new role file. The Orchestrator owns assignments, gates, repair loops, and evidence invalidation. A single runner may perform separate role passes, but must disclose that review is not independent.

## Lifecycle gates
1. Phase 1, clarification: collect requirements before `start work`: clarify scope, acceptance criteria, target, stack, versions, constraints, and manual QA applicability. Keep discussion in chat; write no files and do not populate output folders.
2. Phase 2, execution: begin only when the user sends the standalone command `start work` for an actual project. Quoted commands in reference material do not count. Announce the stack, write `description/01_requirements.md` and `description/02_project_plan.md`, and assign stages.
3. Each required stage loops until its criteria pass. If any review or QA stage reports FAIL, the task returns to the owner (usually the Engineer) and repeats until every check reports PASS. Record failures, owners, attempts, corrective actions, and rerun evidence. Blocked stages never advance just because retries are exhausted.
4. Deliver the project in `work/` and reports in `description/` for user review. This is awaiting acceptance, not final completion.
5. Phase 3, cleanup: only the standalone command `finish work` after delivery authorizes closure. Premature acceptance cannot bypass missing criteria; request acceptance again after delivery. Scope changes reopen affected stages.
6. On `finish work`, empty the contents of both `work/` and `description/` immediately, with no further confirmation, including hidden files and subdirectories. Delete entries without following symlinks, and leave tool-state folders such as `.claude/`. The project and reports are not recoverable afterwards unless the user copied or committed them, so delivery review happens before `finish work`. Verify both folders are empty, then give the closure summary (acceptance, final verification, what was deleted, leftovers) in chat, since `description/` is emptied.

## Token efficiency
- No echoing: never print file contents (code, plans, reports) into chat; write files with tools and say only where they were saved.
- Read only what you need: each role reads its own file, the active stack file, this workflow, and the specific inputs listed in its role file, not the whole chat history.
- Strict handoff format: `[Role] finished. Report saved to [path]. Handing off to [Next Role].` Failures use the same shape: `[Role] reports FAIL. Report saved to [path]. Returning to [Owner].`
- Memory lives in files, not chat history. Agents pass information by reading and writing the numbered reports.

## Stack selection
Line 1 of this file, `Active stack: <name>`, is the single source of truth. `<name>` must be the filename (without `.md`) of an existing file in `stacks/`. The Orchestrator announces the stack and versions in `description/01_requirements.md` and each handoff. Role files contain no stack-specific commands or tools. Supported stacks: `php`, `python`, `go`, `js-ts`. A new stack needs a new `stacks/<name>.md` with the same sections as the existing files (Environment, Testing, Frameworks, Linting, and Supporting Tools, Commands, Quality Checklist) and validated commands before implementation. Multiple stacks require reading every relevant stack file. Never modify role files just to switch stacks.

## Project-local environment
The project is self-contained in `work/`. DevOps provisions the environment there according to the active stack file, and every stage runs commands through it. Nothing is installed on the host: no `sudo`, `apt`, or global package installs, and the Orchestrator never asks the user to install system packages. If the mechanism is unavailable (for example the Docker daemon is unreachable for PHP), DevOps records the exact blocker and the Orchestrator reports it to the user instead of falling back to the host. Record the mechanism and exact commands in `description/04_environment.md`.

## Ordered stages and success criteria
| Stage | Owner | Report | Evidence required to advance |
| --- | --- | --- | --- |
| Requirements and planning | Orchestrator | 01, 02 | User `start work`; testable scope, stack, constraints, target, manual QA decision |
| Architecture | Architect | 03 | Accepted structure, interfaces, decisions, risks, and validation approach |
| Environment | DevOps | 04 | Project-local environment and scaffolding in `work/`; setup and smoke-check run through it; no host installs; no commit or push |
| Implementation and code tests | Engineer + Test Engineer | 05, 06 | Synchronized production code and meaningful core, boundary, and regression tests in `work/`; passing results |
| Review | Reviewer | 07 | approve verdict for identified code and tests; no unresolved blocking findings |
| Automated QA | QA Automation | 08 | Applicable integration/E2E suites pass; reproducible commands and results |
| Manual QA | Manual QA | 09 | Required scenarios pass and sign-off recorded; otherwise explicit reasoned not-required decision |
| Delivery | All members | 01-09 | Project in `work/`, numbered reports and member summaries in `description/` |
| Closure | Orchestrator | chat only | User `finish work` after delivery; both folders emptied and verified; closure summary given in chat |

DevOps follows architecture and precedes engineering. Code and code-level tests proceed together. Review sees both. Automated QA follows approval, manual QA follows automation. A not-required manual QA decision is explicit and still recorded in report 09.

## Loop-back ownership
Design defects return to Architect; environment failures to DevOps; production defects to Engineer; code-test defects to Test Engineer; acceptance suite defects to QA Automation. Findings go through the Orchestrator, with stable ID, severity, reproduction, expected/actual behavior, location, owner, and status.

Changes invalidate dependent evidence. Code or test fixes require code tests and fresh review before affected QA reruns. Design/environment changes reopen all impacted stages. Preserve failed results with superseded labels. Identify reviewed changes by revision, diff, or digest manifest; never apply approval to different content. No unresolved gate failure permits advancement.

## Shared artifacts
| Path | Owner | Contents |
| --- | --- | --- |
| `work/` | Engineer, Test Engineer, DevOps, QA | Actual application source, tests, environment scaffolding, manifests, configuration |
| `work/manual-qa/` | Manual QA | Executable helpers or fixtures only, when needed; reports belong in `description/` |
| `description/01_requirements.md` | Orchestrator | Scope, acceptance criteria, target, stack/version, constraints, user `start work`, QA applicability |
| `description/02_project_plan.md` | Orchestrator | Stage plan, current stage, owners, attempts, gate evidence, blockers, invalidated approvals, handoffs, delivery summary |
| `description/03_architecture_plan.md` | Architect | Design, module layout, interfaces, decisions, risk and verification plan |
| `description/04_environment.md` | DevOps | Setup instructions, runtime versions, commands, smoke-check results |
| `description/05_engineer_report.md` | Engineer | Behavior changes, requirement mapping, change set (paths, baseline, diff or digest), deviations, limitations |
| `description/06_test_report.md` | Test Engineer | Requirement-to-test map, core/boundary cases, exact commands, environment, counts, outcomes, regression evidence |
| `description/07_review_report.md` | Reviewer | Change identity, approve/request-changes verdict, findings and closure evidence |
| `description/08_qa_automation_report.md` | QA Automation | Integration/E2E scope, commands, results, sanitized evidence |
| `description/09_manual_qa_report.md` | Manual QA | Manual scope, scenarios, environment, observations, defects, retests, sign-off or not-required decision |
| `description/evidence/` | Any role | Optional generated coverage, result, and log files; created only when needed |
| Closure summary (chat only) | Orchestrator | Actual user acceptance, final verification, what was deleted, leftovers. Not written to `description/`, which is emptied on `finish work`. |

Each role's numbered report is also its final member summary: work performed, changed files, verification, limitations. Role document paths resolve relative to their role directory (`agents/`). Report names resolve under `description/`; source and test paths resolve under `work/`. Never place reports inside the application project. Create files on demand when their stage runs; never create later numbers early.

## Target repository and delivery
Inspect the user-provided target's rules and baseline before changing code. Build the task's actual project in `work/`, preserving its native layout. Record any separately requested integration destination in `description/01_requirements.md`; do not overwrite unrelated user changes. Capture a reviewable diff or manifest. Do not include credentials or dependency caches in portable delivery.

## Cleanup contract
After user acceptance (standalone `finish work`), re-run the final verification, then remove the contents of `work/` and `description/` only (no other paths), including hidden entries. Never follow symlinks for deletion, and leave tool-state folders such as `.claude/`. Inspect each target first, then verify both folders are empty and report anything left. Give the closure summary in chat. This is irreversible unless the user copied or committed the outputs. Starting a new project requires both folders to be empty.

## Definition of Done
Every required stage passes, review approves code and tests, automated QA is green, manual QA signs off or is explicitly not required, all numbered reports are written, the user sends `finish work` after reviewing delivery, and both output folders are emptied and verified. Until then report the actual state without claiming final completion.
