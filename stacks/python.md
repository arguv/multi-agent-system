# Python Stack

Selected when `Active stack: python` is set at the top of `../workflow.md`. Every role reads this file before starting work. Commands run from the project root (`work/`), after dependencies are installed, through the project-local environment.

## Environment
Python 3.10+; use repository constraints. Everything stays in `work/`: never use system `pip`. Run `python -m venv .venv`, activate with `. .venv/bin/activate` (POSIX), then `python -m pip install -r requirements.txt`.

## Testing
pytest: `python -m pytest`; verbose: `python -m pytest -v`; one file: `python -m pytest tests/test_example.py`; coverage with pytest-cov: `python -m pytest --cov=package`.

## Frameworks, Linting, and Supporting Tools
unittest, unittest.mock, Hypothesis, Coverage.py; Ruff and type checks when configured.

## Role Application
Apply each role's Core Skills to this stack. Use framework-specific setup only when the architecture selects it. For automation, run integration/E2E tools appropriate to the product; code-level tests alone do not establish end-to-end acceptance. For manual QA, exercise the running service, CLI, or UI and record runtime and platform versions.

## Commands
| Install deps | Run tests | Lint / check |
| --- | --- | --- |
| `python -m pip install -r requirements.txt` | `python -m pytest` | `python -m ruff check .` if installed |

## Quality Checklist
- [ ] Runtime and dependency versions match the accepted environment.
- [ ] Commands exist in the target repository and pass, or blockers are reported.
- [ ] Relevant logic, integration boundaries, and failure behavior have evidence.
