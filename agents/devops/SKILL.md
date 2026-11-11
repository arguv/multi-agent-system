---
name: devops-skills
description: "DevOps Engineer stack-specific capabilities. Covers PHP (PHPUnit, Composer), Python (pytest, venv), Go (testing, Testify, go.mod), and JS/TS (Vitest, Jest). Use when performing the devops role."
---

# DevOps Engineer — Skills

## Core Skills (stack-independent)
- Before work, read `instructions.md` and this section, then only the announced stack section(s), command row(s), and the all-stack checklist.
- Prepare isolated, reproducible environments, dependency manifests, lock files where appropriate, configuration examples, and health checks. Record setup commands and version constraints. Never commit or push; never include credentials.
- Follow `../../workflow.md`; report evidence and blockers without inventing results.
- Build source, tests, and scaffolding in `../../work/`. Write all plans, reports, logs, and summaries to `../../description/`. Keep both folders empty before an actual project starts; framework maintenance must not generate project outputs.
- Commands below are examples run from the target root (`../../work/`), after dependencies are installed. Prefer existing scripts and pinned tools. Do not install every supporting tool.
- PHP is the active application stack. Python, Go, JS/TS, and framework-maintenance Markdown sections are preserved inside HTML comments and must not be used for this PHP project. To switch later, uncomment the selected section and command row, and comment the previously active ones. Unknown stacks require a documented capability extension before proceeding.

<!-- Inactive: Markdown
## Markdown Stack
### Environment
Plain UTF-8 Markdown; no application runtime or dependency installation is required.
### Primary Validation
Inspect frontmatter, relative references, workflow contracts, and role completeness. Run the repository's structural checker if supplied; use Python only as a validation utility.
### Supporting Tools
A text editor and dependency-free structural checks. Read-through scenarios validate lifecycle behavior; do not claim runtime integration from static checks.
### Quality Checklist
- [ ] Canonical content remains portable and instructions remain stack-independent.
- [ ] Role contracts and lifecycle scenarios are internally consistent.
- [ ] Structural checks and manual document review have recorded outcomes.
-->

## PHP Stack
### Environment
PHP 8.3+ and Composer; use repository version constraints. Run `composer install`.
### Primary Test Framework
PHPUnit: `vendor/bin/phpunit`; one file: `vendor/bin/phpunit tests/ExampleTest.php`; selection: `vendor/bin/phpunit --filter testName`.
### Supporting Tools
Mockery, Codeception, or Pest when already selected; PHPStan and PHP_CodeSniffer when configured.
### Role Application
Composer manifests and lock file; `.env.example` without secrets; PHP runtime/extensions and service setup documented.
Apply the role's Core Skills to this stack. Use framework-specific setup only when selected in the architecture.
For automation, run integration/E2E tools appropriate to the product; code-level tests alone do not establish end-to-end acceptance.
For manual QA, exercise the running service, CLI, or UI and record runtime and platform versions.
### Quality Checklist
- [ ] Runtime and dependency versions match the accepted environment.
- [ ] Commands exist in the target repository and pass, or blockers are reported.
- [ ] Relevant logic, integration boundaries, and failure behavior have evidence.

<!-- Inactive: Python
## Python Stack
### Environment
Python 3.10+; use repository constraints. Run `python -m venv .venv`, activate with `. .venv/bin/activate` (POSIX), then `python -m pip install -r requirements.txt`.
### Primary Test Framework
pytest: `python -m pytest`; verbose: `python -m pytest -v`; one file: `python -m pytest tests/test_example.py`; coverage with pytest-cov: `python -m pytest --cov=package`.
### Supporting Tools
unittest, unittest.mock, Hypothesis, Coverage.py; Ruff and type checks when configured.
### Role Application
Document `.venv` setup; maintain `requirements.txt` and a separate development dependency manifest when needed; ignore generated environments.
Apply the role's Core Skills to this stack. Use framework-specific setup only when selected in the architecture.
For automation, run integration/E2E tools appropriate to the product; code-level tests alone do not establish end-to-end acceptance.
For manual QA, exercise the running service, CLI, or UI and record runtime and platform versions.
### Quality Checklist
- [ ] Runtime and dependency versions match the accepted environment.
- [ ] Commands exist in the target repository and pass, or blockers are reported.
- [ ] Relevant logic, integration boundaries, and failure behavior have evidence.
-->

<!-- Inactive: Go
## Go Stack
### Environment
Go 1.21+; follow the go.mod directive. Run `go mod download` and `go build ./...`.
### Primary Test Framework
Standard testing in `*_test.go`: `go test ./...`; selection: `go test ./path -run TestName`; race detection where supported: `go test -race ./...`.
### Supporting Tools
Testify, gomock, testcontainers, autogold, or rapid when justified; `go vet ./...` and `gofmt`.
### Role Application
Maintain go.mod and go.sum; initialize go.mod with the agreed module path only when absent; document native prerequisites.
Apply the role's Core Skills to this stack. Use framework-specific setup only when selected in the architecture.
For automation, run integration/E2E tools appropriate to the product; code-level tests alone do not establish end-to-end acceptance.
For manual QA, exercise the running service, CLI, or UI and record runtime and platform versions.
### Quality Checklist
- [ ] Runtime and dependency versions match the accepted environment.
- [ ] Commands exist in the target repository and pass, or blockers are reported.
- [ ] Relevant logic, integration boundaries, and failure behavior have evidence.

### Table-Driven Test Pattern
```go
func TestNormalize(t *testing.T) {
    cases := []struct { name, input, want string }{
        {name: "trim spaces", input: " x ", want: "x"},
        {name: "empty", input: "", want: ""},
    }
    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            if got := Normalize(tc.input); got != tc.want {
                t.Fatalf("Normalize(%q) = %q; want %q", tc.input, got, tc.want)
            }
        })
    }
}
```
Illustrative structure: replace `Normalize` with the project's real API and import `testing`.
-->

<!-- Inactive: JS/TS
## JS/TS Stack
### Environment
Use the repository Node.js version and package manager. With a package-lock.json use `npm ci`; for a new npm project use `npm install` and retain the lock file.
### Primary Test Framework
Vitest or Jest as selected by the repository; expose `npm test`. Vitest file: `npx vitest run tests/example.test.ts`; Jest file: `npx jest tests/example.test.ts`.
### Supporting Tools
Playwright or Cypress for browser E2E when applicable; ESLint and TypeScript checks when configured.
### Role Application
Maintain package.json and one package-manager lock file; document runtime, scripts, build, and configuration examples.
Apply the role's Core Skills to this stack. Use framework-specific setup only when selected in the architecture.
For automation, run integration/E2E tools appropriate to the product; code-level tests alone do not establish end-to-end acceptance.
For manual QA, exercise the running service, CLI, or UI and record runtime and platform versions.
### Quality Checklist
- [ ] Runtime and dependency versions match the accepted environment.
- [ ] Commands exist in the target repository and pass, or blockers are reported.
- [ ] Relevant logic, integration boundaries, and failure behavior have evidence.
-->

## Tooling Commands (quick reference)
| Stack | Install deps | Run tests | Lint / check |
| --- | --- | --- | --- |
| PHP | `composer install` | `vendor/bin/phpunit` | configured PHPStan / PHP_CodeSniffer commands |

<!-- Inactive stack commands
| Python | `python -m pip install -r requirements.txt` | `python -m pytest` | `python -m ruff check .` if installed |
| Go | `go mod download` | `go test ./...` | `go vet ./...`; `gofmt -l .` |
| JS/TS | `npm ci` with lock file | `npm test -- --runInBand` for Jest; `npx vitest run` for Vitest | configured lint and typecheck scripts |
-->

## Quality Checklist (all stacks)
- [ ] Own instructions and matching stack skills read before acting.
- [ ] Inputs and handoff are current and complete.
- [ ] Selected commands, prerequisites, results, and limitations are recorded.
- [ ] No credentials, dependency caches, or generated environments enter the delivery.
- [ ] Role success criteria are met or explicit blockers are returned.
- [ ] Reports are in `../../description/`; project files are in `../../work/`.
- [ ] Per-member summary is ready before user review; cleanup preserves project and reports.
