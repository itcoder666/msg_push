from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class PushPlusResult:
    code: int | None
    message: str


class PushPlusError(RuntimeError):
    """Raised when PushPlus rejects or cannot process a message."""


def build_pushplus_payload(
    token: str,
    title: str,
    content: str,
    *,
    topic: str | None = None,
) -> dict[str, str]:
    if not token:
        raise PushPlusError("PUSHPLUS_TOKEN is required")

    payload = {
        "token": token,
        "title": title,
        "content": content,
    }
    if topic:
        payload["topic"] = topic
        print(f"pushplus topic: {topic}")

    return payload


def send_pushplus_message(
    *,
    token: str,
    title: str,
    content: str,
    url: str,
    topic: str | None = None,
    timeout: int = 10,
) -> PushPlusResult:
    payload = build_pushplus_payload(token, title, content, topic=topic)
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            raw_response = response.read().decode("utf-8")
            result = json.loads(raw_response)
    except URLError as exc:
        raise PushPlusError(f"Failed to send PushPlus message: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise PushPlusError("PushPlus returned invalid JSON") from exc

    code = result.get("code")
    message = str(result.get("msg") or result.get("message") or result)
    data = result.get("data")
    if data is not None:
        message = f"{message}, data={data}"
    if code != 200:
        raise PushPlusError(f"PushPlus send failed: code={code}, message={message}")

    return PushPlusResult(code=code, message=message)
