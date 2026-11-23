# Shared Workflow and Artifact Contract

## Folder contract
All paths here are relative to the repository root.
- `work/` is the actual user project: source code, tests, dependency manifests, configuration, and project scaffolding. For a weather project, its application is built directly here, not in a nested delivery directory.
- `description/` contains every task document and agent report: requirements, architecture, setup notes, handoffs, reviews, test results, QA reports, and final member summaries.
Both folders remain empty until an actual user project is started. Framework maintenance never creates task outputs. Empty folders may be absent after a fresh Git checkout; create them on demand when the project starts, without placeholder reports. Building or installing this team framework does not populate them. Create report subdirectories only when needed. Missing future-stage reports are normal; never fabricate them to satisfy a reference. Do not prefill success reports or sample task results.

## Authority and pre-work
The coordinating agent starts as the Orchestrator automatically through AGENTS.md; no user startup prompt or file-reading list is required. A delegated worker follows its assigned role instead. Project descriptions begin requirements collection; only work start begins delivery stages.
Every member reads its own `agents/<role>/instructions.md` and `agents/<role>/SKILL.md` before work. Read Core Skills, matching stack sections and command rows, and the all-stack checklist. Read this workflow and current task inputs. Role switches require the new role pair. The Orchestrator owns assignments, gates, repair loops, and evidence invalidation. A single runner may perform separate role passes, but must disclose that review is not independent.

## Lifecycle gates
1. Collect requirements before `work start`: clarify scope, acceptance criteria, target, stack, versions, constraints, and manual QA applicability. Keep discussion in chat; do not populate output folders yet.
2. Begin only when the user sends standalone `work start` for an actual project. Quoted commands in reference material do not count. Announce the stack, write description/task.md, and assign stages.
3. Each required stage loops until its criteria pass. Record failures, owners, attempts, corrective actions, and rerun evidence. Blocked stages never advance just because retries are exhausted.
4. Deliver the project in work/ and reports in description/ for user review. This is awaiting acceptance, not final completion.
5. Only standalone `work done` after delivery authorizes closure. Premature acceptance cannot bypass missing criteria; request acceptance again after delivery. Scope changes reopen affected stages.
6. Cleanup: On `work done`, empty the contents of both `work/` and `description/` immediately, with no further confirmation. Delete entries without following symlinks, and leave tool-state folders such as `.claude/`. The project and reports are not recoverable afterwards unless the user copied or committed them, so delivery review happens before `work done`. Give the closure summary (acceptance, final verification, what was deleted, leftovers) in chat, since `description/` is emptied.

## Stack selection
The Orchestrator announces selected technology, runtime constraints, and frameworks in description/task.md and each handoff. Support PHP, Python, Go, and JS/TS using the matching skill sections. Multiple stacks require all relevant sections. PHP is currently active; Python, Go, and JS/TS sections and their command rows are commented out. Before switching stacks, uncomment the selected sections and rows and comment the previously active ones. Unsupported stacks need documented capability support and validated commands before implementation. Never modify stable instructions just to switch stacks.

## Project-local environment
The project is self-contained in `work/`. DevOps provisions the environment there and every stage runs commands through it. PHP uses Docker (`Dockerfile`, `compose.yaml`, `dev` wrapper in `work/`); Python uses `.venv`; Go uses a project-local `GOPATH`/`GOMODCACHE`; JS/TS uses local `node_modules` with a pinned Node. Nothing is installed on the host: no `sudo`, `apt`, or global package installs, and the Orchestrator never asks the user to install system packages. If the mechanism is unavailable (for example the Docker daemon is unreachable), DevOps records the exact blocker and the Orchestrator reports it to the user instead of falling back to the host. Record the mechanism and exact commands in description/environment.md.

## Ordered stages and success criteria
| Stage | Owner | Evidence required to advance |
| --- | --- | --- |
| Requirements | Orchestrator | User start; testable scope, stack, constraints, target, manual QA decision |
| Architecture | Architect | Accepted structure, interfaces, decisions, risks, and validation approach |
| Environment | DevOps | Project-local environment (Docker for PHP, `.venv` for Python, etc.) and scaffolding in work/; setup and smoke-check run through it; report; no host installs; no commit or push |
| Implementation and code tests | Engineer + Test Engineer | Synchronized production code and meaningful core, boundary, and regression tests in work/; passing results |
| Review | Reviewer | approve verdict for identified code and tests; no unresolved blocking findings |
| Automated QA | QA Automation | Applicable integration/E2E suites pass; reproducible commands and results |
| Manual QA | Manual QA | Required scenarios pass and sign-off recorded; otherwise explicit reasoned not-required decision |
| Delivery | All members | Project in work/, all reports and eight member summaries in description/ |
| Closure | Orchestrator | User work done after delivery; both folders emptied and verified; closure summary given in chat |

DevOps follows architecture and precedes engineering. Code and code-level tests proceed together. Review sees both. Automated QA follows approval, manual QA follows automation. A not-required manual QA decision is explicit and still has a member summary.

## Loop-back ownership
Design defects return to Architect; environment failures to DevOps; production defects to Engineer; code-test defects to Test Engineer; acceptance suite defects to QA Automation. Findings go through the Orchestrator, with stable ID, severity, reproduction, expected/actual behavior, location, owner, and status.

Changes invalidate dependent evidence. Code or test fixes require code tests and fresh review before affected QA reruns. Design/environment changes reopen all impacted stages. Preserve failed results with superseded labels. Identify reviewed changes by revision, diff, or digest manifest; never apply approval to different content. No unresolved gate failure permits advancement.

## Shared artifacts
| Path | Contents |
| --- | --- |
| `work/` | Actual application source, tests, environment scaffolding, manifests, configuration |
| `work/manual-qa/` | Manual QA executable helpers or fixtures only, when needed; reports belong in description/ |
| `description/task.md` | Scope, acceptance criteria, target, stack/version, constraints, user start, QA applicability |
| `description/status.md` | Current stage, owners, attempts, gate evidence, blockers, invalidated approvals |
| `description/handoffs.md` | Assignments, stack, inputs, outputs, criteria, dependencies, findings |
| `description/architecture.md` | Design, module layout, interfaces, decisions, risk and verification plan |
| `description/environment.md` | Setup instructions, runtime versions, commands, smoke-check results |
| `description/implementation.md` | Behavior changes, requirement mapping, deviations, limitations |
| `description/change-set.md` | Changed project-relative paths, baseline, diff or digest identity |
| `description/test-plan.md` | Requirement-to-test map, core/boundary cases, integration/E2E scope |
| `description/review.md` | Change identity, approve/request-changes verdict, findings and closure evidence |
| `description/reports/code-tests.md` | Exact commands, environment, counts, outcomes, regression evidence; generated coverage and test-result files also belong under description/reports/ |
| `description/reports/automation.md` | Integration/E2E commands, results, sanitized evidence |
| `description/manual-qa/plan.md` | Manual scope, scenarios, environment, expected behavior |
| `description/manual-qa/results/report.md` | Observations, defects, retests, sign-off or not-required decision |
| `description/<role>.md` | One final member summary: work performed, changed files, verification, limitations |
| Closure summary (chat only) | Actual user acceptance, final verification, what was deleted, leftovers. Not written to description/, which is emptied on work done. |

Role document paths resolve relative to their role directory. Report names listed in role inputs and outputs resolve under description/; source/test paths resolve under work/. Never place reports inside the application project.

## Target repository and delivery
Inspect the user-provided target's rules and baseline before changing code. Build the task's actual project in work/, preserving its native layout. Record any separately requested integration destination in description/task.md; do not overwrite unrelated user changes. Capture a reviewable diff or manifest. Do not include credentials or dependency caches in portable delivery.

## Cleanup contract
After user acceptance (standalone `work done`), re-run the final verification, then remove the contents of `work/` and `description/` only (no other paths). Never follow symlinks for deletion, and leave tool-state folders such as `.claude/`. Inspect each target first, then verify both folders are empty and report anything left. Give the closure summary in chat. This is irreversible unless the user copied or committed the outputs. Starting a new project requires both folders to be empty.

## Definition of Done
Every required stage passes, review approves code and tests, automated QA is green, manual QA signs off or is explicitly not required, eight summaries are written, the user sends work done after reviewing delivery, and both output folders are emptied and verified. Until then report the actual state without claiming final completion.
