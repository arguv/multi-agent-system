# PHP Stack

Selected when `Active stack: php` is set at the top of `../workflow.md`. Every role reads this file before starting work. Commands run from the project root (`work/`), after dependencies are installed, through the project-local environment.

## Environment
Docker is the project-local environment. DevOps writes `Dockerfile` (pinned PHP version and required extensions, Composer included), `compose.yaml`, and a `dev` wrapper script into `work/`, so `./dev <command>` runs `docker compose run --rm app <command>` with `work/` mounted. Use PHP 8.3+ unless the repository constrains otherwise. Dependencies install into `work/vendor`. Check `docker info` first; if the daemon is unreachable, report the blocker (do not install PHP on the host). Install with `./dev composer install`.

## Testing
PHPUnit: `vendor/bin/phpunit`; one file: `vendor/bin/phpunit tests/ExampleTest.php`; selection: `vendor/bin/phpunit --filter testName`.

## Frameworks, Linting, and Supporting Tools
Mockery, Codeception, or Pest when already selected; PHPStan and PHP_CodeSniffer when configured.

## Role Application
Apply each role's Core Skills to this stack. Use framework-specific setup only when the architecture selects it. For automation, run integration/E2E tools appropriate to the product; code-level tests alone do not establish end-to-end acceptance. For manual QA, exercise the running service, CLI, or UI and record runtime and platform versions.

## Commands
| Install deps | Run tests | Lint / check |
| --- | --- | --- |
| `./dev composer install` | `./dev vendor/bin/phpunit` | `./dev` plus configured PHPStan / PHP_CodeSniffer commands |

## Quality Checklist
- [ ] Runtime and dependency versions match the accepted environment.
- [ ] Commands exist in the target repository and pass, or blockers are reported.
- [ ] Relevant logic, integration boundaries, and failure behavior have evidence.
- [ ] `Dockerfile`, `compose.yaml`, and the `dev` wrapper are present in `work/`; `.env.example` has no secrets.
