# CLAUDE.md

This project sends a daily USD/CNY exchange-rate notification through any configured notification channels.

Supported channels:

- PushPlus
- WeChat Work group robot
- WxPusher

## Project conventions

- Use the Python `src` layout. Application code lives in `src/msg_push/`.
- Keep network I/O separated from parsing/formatting logic so unit tests do not need live services.
- Keep each notification channel in its own module and route orchestration through `src/msg_push/notifiers.py`.
- Prefer small pure functions with type annotations.
- Use only the Python standard library for runtime code unless a dependency is clearly justified.
- Do not commit local virtual environments, `.env`, cache directories, or generated artifacts.

## Security rules

- Never hard-code tokens, webhook URLs, or any other secret.
- Never print secrets to logs, test output, GitHub Actions logs, README, or examples.
- Use GitHub repository secrets for production tokens and webhook URLs.
- Treat PushPlus, WeChat Work, WxPusher, and external exchange-rate API responses as untrusted data.

## Notification configuration

A channel is enabled when its required environment variables are configured:

- PushPlus: `PUSHPLUS_TOKEN` (optionally `PUSHPLUS_TOPIC` for one-to-many group messages)
- WeChat Work group robot: `WECHAT_WORK_WEBHOOK_URL`
- WxPusher: `WXPUSHER_APP_TOKEN` plus at least one of `WXPUSHER_UIDS` or `WXPUSHER_TOPIC_IDS`

If multiple channels are configured, the app must attempt all of them. A failure in one channel should not prevent attempts to send through the remaining configured channels.

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

The workflow in `.github/workflows/exchange-rate-push.yml` runs daily at 01:00 UTC, which is 09:00 in Asia/Shanghai. Configure the repository secrets for whichever notification channels should be enabled.
