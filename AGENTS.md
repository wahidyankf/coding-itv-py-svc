# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project

`coding-itv-py` is a monorepo with three apps in `apps/`: `super-web` (Next.js), `super-be` (FastAPI), and `super-web-e2e` (Playwright). Shared tooling and rules are at the root.

## Repository setup

- Git uses `main` as the default branch. It is pushed to `origin` at `git@github.com:wahidyankf/coding-itv-py-svc.git`. Do not delete or use `master`; it is an old remote branch.
- `package.json` comes from `npm init -y`. Its `test` script is still npm's placeholder.
- Node is pinned to 24.22.0 (the current LTS) with Volta, in the `volta` field of `package.json`. `engines` requires `>=24.22.0`. Use Volta so the pinned version is used automatically.
- Prettier formats JS, JSON, Markdown, and YAML. Husky runs `lint-staged` from `.husky/pre-commit` on commit, and lint-staged runs `prettier --write` on the staged files. Run `npm install` after cloning so the hooks get installed by the `prepare` script.
- Commit messages must follow Conventional Commits. `.husky/commit-msg` runs commitlint with `@commitlint/config-conventional`, configured in `commitlint.config.js`. Allowed types are build, chore, ci, docs, feat, fix, perf, refactor, revert, style, and test.
- The repo is an Nx workspace. The npm workspaces are `apps/super-web` and `apps/super-web-e2e`, listed in the root `package.json`. One root `package-lock.json` covers them. `apps/super-be` is not an npm workspace; it uses uv. `nx.json` is the workspace config. `apps/` and `libs/` are at the root.
- Do not install or use Nx plugins (`@nx/*`, `nx-*` packages, or plugin entries in `nx.json`). Define every target in a `project.json` with `"executor": "nx:run-commands"` and a `command` option. Do not use `nx init`, which can add plugins.
- Every app in `apps/` has a `project.json` with the same target set. Run targets with `npx nx <target> <app>`, for example `npx nx test:quick super-be`.
  - `typecheck`: `tsc --noEmit` for TypeScript apps, `pyright` for `super-be`.
  - `lint`: Biome for the TypeScript apps, `ruff check` for `super-be`. Biome is configured in the root `biome.json`. It only lints; Prettier formats. It skips `public/` because those are static assets.
  - `test:unit` and `test:unit:watch`: Vitest for `super-web`, pytest and pytest-watcher for `super-be`.
  - `test:e2e` and `test:e2e:watch`: Playwright, for `super-web-e2e` only.
  - `dev`: starts the dev server, for `super-web` and `super-be` only.
  - `start`: runs the production server. For `super-web` it runs `next start` after `build`. For `super-be` it runs uvicorn without reload, and it has no build step.
  - Extra targets: `build` (`super-web` only) and `format` (`super-be`, `ruff format --check`).
  - `test:quick`: runs the same app's `typecheck`, `lint`, and `test:unit` targets, in that order, through `npx nx <target> <app>`. Change a check in its own target, not in `test:quick`. `super-web-e2e` has no `test:unit`, so its `test:quick` runs `typecheck` and `lint`.
- The pre-commit hook also runs `ruff format` on staged Python files in `apps/super-be` (configured under `lint-staged` in `package.json`). It formats only; it does not run `ruff check`.
- `.husky/pre-push` runs `npx nx affected -t test:quick --base=origin/main`, so a push runs `test:quick` only for projects changed since the last state on `origin/main`. Local `main` is not used as the base, because it already includes the commits being pushed. Do not skip it with `--no-verify` unless the user asks.
- TypeScript apps must reject implicit `any`. Keep `noImplicitAny: true` set explicitly in each `tsconfig.json`.
- `apps/super-web` is a Next.js App Router app in TypeScript. Unit tests use Vitest with jsdom and Testing Library, in `*_tests.tsx` files next to the code (see Tests below). Vitest globals are off, so call `cleanup` in `afterEach` when rendering components. It is an npm workspace, so install its dependencies from the root. Use `typescript` 7.x, the same version in both web apps. Keep `@types/node` on 24 to match the Node pin.
- `apps/super-be` is a FastAPI app in Python 3.13+, managed with uv. Its package is `super_be/`, and its tests sit next to the source as `*_tests.py` (see Tests below). Ruff and pyright are configured in `pyproject.toml`. Run `uv run ruff format .` to fix formatting. Commit `uv.lock`.
- `apps/super-web-e2e` has Playwright tests in `tests/`. The Playwright config builds and starts `super-web` on port 3000 if it isn't already running, waits for `/api/health` to return, and then runs the tests against the production build.

## Tests

- Use TDD (test-driven development) for every code change. Follow Red - Green - Refactor: write a failing test first (Red), write the least code to make it pass (Green), then clean up the code while the tests stay green (Refactor). Run the test to see it fail before you write the code, so you know it tests the right thing.
- Unit tests live next to the source file, named `*_tests.ts`, `*_tests.tsx`, or `*_tests.py`. `super-web` runs them with Vitest and `super-be` with pytest, so the tests use those runners, not Node's built-in runner.
- Config checks that apply only in production mode use `*_production_tests.*`. The `test:unit` targets skip them. Use this name for production-only assertions, not for general unit tests.
- Test files are excluded from type-aware linting. Biome lint is not type-aware in this repo yet, so apply this when type-aware linting is added. Type errors are caught by `typecheck`.
- E2E tests use Playwright and run against a real server. Playwright starts the server and waits for `GET /api/health` before the tests run. Keep `/api/health` working, because the e2e setup depends on it.
- `.gitignore` covers Python, Node.js, Nx cache (`.nx/`), Next.js and test output (`.next/`, `.vitest/`, `test-results/`, `playwright-report/`), env files, and local tool settings. Add new tool output there, not in per-app ignore files.

## Agent skills

- `grill-me` is in `.agents/skills/grill-me/SKILL.md`. Its copy in `.claude/skills/grill-me/SKILL.md` points to the `.agents` copy. It comes from `wahidyankf/ose-rules`. Use it before a material choice that has more than one reasonable answer.

## Conventions

- Do not add Claude co-author attribution to commits. `.claude/settings.json` sets `includeCoAuthoredBy: false` for this project. Keep that setting.
- `.claude/settings.local.json` is machine-local and ignored by git. Do not commit it.
- Do not commit or push unless the user asks.
- Make commits thematically. Each commit should contain one coherent change, such as one tool setup or one feature, and should not mix unrelated files. Stage files by theme, and make a separate commit for each theme, rather than one commit for everything in the working tree.

## Code style

- Keep comments, commit messages, and notes brief.
- Explain why the code is needed, not what it does.
- Use clear, simple, and natural English that is easy for non-native speakers to understand.

## Architecture

### Config & secrets

- Config is built once from `process.env`, at import time.
- The build function is also exported separately, for testing.
- In production, if a required security env var is missing or invalid, the app fails fast.
