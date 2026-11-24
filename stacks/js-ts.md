# JS/TS Stack

Selected when `Active stack: js-ts` is set at the top of `../workflow.md`. Every role reads this file before starting work. Commands run from the project root (`work/`), after dependencies are installed, through the project-local environment.

## Environment
Use the repository Node.js version and package manager. Pin Node (`.nvmrc` and `engines`), install only into local `node_modules` (no global installs, run tools with `npx`); if the pinned Node is not available, run it from a `node:<version>` Docker image through a `dev` wrapper. With a package-lock.json use `npm ci`; for a new npm project use `npm install` and retain the lock file.

## Testing
Vitest or Jest as selected by the repository; expose `npm test`. Vitest file: `npx vitest run tests/example.test.ts`; Jest file: `npx jest tests/example.test.ts`.

## Frameworks, Linting, and Supporting Tools
Playwright or Cypress for browser E2E when applicable; ESLint and TypeScript checks when configured.

## Role Application
Apply each role's Core Skills to this stack. Use framework-specific setup only when the architecture selects it. For automation, run integration/E2E tools appropriate to the product; code-level tests alone do not establish end-to-end acceptance. For manual QA, exercise the running service, CLI, or UI and record runtime and platform versions.

## Commands
| Install deps | Run tests | Lint / check |
| --- | --- | --- |
| `npm ci` with lock file | `npm test -- --runInBand` for Jest; `npx vitest run` for Vitest | configured lint and typecheck scripts |

## Quality Checklist
- [ ] Runtime and dependency versions match the accepted environment.
- [ ] Commands exist in the target repository and pass, or blockers are reported.
- [ ] Relevant logic, integration boundaries, and failure behavior have evidence.
