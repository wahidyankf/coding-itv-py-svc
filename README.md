# coding-itv-py-svc

A skeleton project for software engineer coding interviews focused on Python services. It is a small monorepo with a working FastAPI backend, a Next.js frontend, and end-to-end tests. Use it as a starting point: read the code, run the checks, and then build or fix the service feature the interview asks for.

## What is inside

| App                  | Stack                            | Purpose                                                          |
| -------------------- | -------------------------------- | ---------------------------------------------------------------- |
| `apps/super-be`      | FastAPI, Python 3.13+, uv        | Python service backend. This is the main area for the interview. |
| `apps/super-web`     | Next.js (App Router), TypeScript | Web frontend.                                                    |
| `apps/super-web-e2e` | Playwright                       | End-to-end tests against the running web app.                    |

The apps are managed with [Nx](https://nx.dev). Nx only runs commands; no Nx plugins are used. Each app has the same set of targets in its `project.json`.

## Prerequisites

- [Volta](https://volta.sh), which installs the pinned Node.js version (24.22.0) for this repo.
- [uv](https://docs.astral.sh/uv/), which manages Python and the `super-be` dependencies.
- Git.

## Getting started

```sh
# Install the root tooling, Git hooks, and the frontend and e2e dependencies (npm workspaces)
npm install

# Install the backend dependencies
cd apps/super-be && uv sync && cd ../..
```

## Common commands

Run a target for one app with `npx nx <target> <app>`:

```sh
npx nx dev super-be             # backend with reload at http://localhost:8000
npx nx dev super-web            # frontend at http://localhost:3000
npx nx test:unit super-be       # pytest
npx nx test:quick super-be      # typecheck + lint + unit tests
npx nx test:e2e super-web-e2e   # Playwright (starts the web app for you)
```

Other targets:

- `typecheck`: `pyright` for `super-be`, `tsc --noEmit` for the TypeScript apps.
- `lint`: `ruff check` for `super-be`, Biome for the TypeScript apps. Biome config is in the root `biome.json`.
- `format`: `ruff format --check` for `super-be`. Run `uv run ruff format .` inside `apps/super-be` to fix formatting.
- `test:unit:watch`, `test:e2e:watch`: rerun tests on change.
- `test:quick:watch`: rerun `typecheck`, `lint`, and unit tests on each change, and show the errors in the terminal.
- `start`: run the production server. `super-web` builds first.

The backend health check is `GET /health`, and the web app's is `GET /api/health`.

## Manual API checks

[`api.http`](api.http) lists requests for the running apps. Open it in an editor with the kulala.nvim plugin, or use any
client that reads `.http` files. Start the app first, then send a request. In Neovim, put the cursor on a request and press `,rh`.

Add a new request as its own `###` block. Keep the host in a variable at the top of the file. This file is for manual checks only. Automated checks go in `*_tests.*` files.

## Layout

```
apps/
  super-be/          FastAPI app
    super_be/        package code, with tests next to it (*_tests.py)
    pyproject.toml   dependencies, pytest, ruff, and pyright config
  super-web/         Next.js app
    app/             routes and components, with tests next to them (*_tests.tsx)
  super-web-e2e/     Playwright tests (tests/)
libs/                shared code for future use (empty for now)
```

## Working rules

- Tests live next to the code. Name them `*_tests.py`, `*_tests.ts`, or `*_tests.tsx`.
- Production-only config checks use `*_production_tests.*`. The unit test runs skip them.
- Commits must follow [Conventional Commits](https://www.conventionalcommits.org). A commit-msg hook checks this.
- The pre-commit hook formats staged files (Prettier for web files, `ruff format` for Python in `super-be`).
- The pre-push hook runs `test:quick` on the projects changed since `main`.

The file [`AGENTS.md`](AGENTS.md) has more detail for AI coding agents and for the repo's full rules.
