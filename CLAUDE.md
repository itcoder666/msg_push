# CLAUDE.md

This project sends a daily USD/CNY exchange-rate notification to WeChat via PushPlus.

## Project conventions

- Use the Python `src` layout. Application code lives in `src/msg_push/`.
- Keep network I/O separated from parsing/formatting logic so unit tests do not need live services.
- Prefer small pure functions with type annotations.
- Use only the Python standard library for runtime code unless a dependency is clearly justified.
- Do not commit local virtual environments, `.env`, cache directories, or generated artifacts.

## Security rules

- Never hard-code `PUSHPLUS_TOKEN` or any other secret.
- Never print secrets to logs, test output, GitHub Actions logs, README, or examples.
- Use GitHub repository secrets for production tokens.
- Treat PushPlus responses and external exchange-rate API responses as untrusted data.

## Common commands

Install for development:

```bash
python -m pip install -e .[dev]
```

Run locally:

```bash
python -m msg_push
```

Run tests:

```bash
pytest
```

Run lint:

```bash
ruff check .
```

## GitHub Actions

The workflow in `.github/workflows/exchange-rate-push.yml` runs daily at 01:00 UTC, which is 09:00 in Asia/Shanghai. It requires the repository secret `PUSHPLUS_TOKEN`.
