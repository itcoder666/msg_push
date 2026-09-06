from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class WxPusherResult:
    code: int | None
    message: str


class WxPusherError(RuntimeError):
    """Raised when WxPusher rejects or cannot process a message."""


def build_wxpusher_payload(
    *,
    app_token: str,
    summary: str,
    content: str,
    uids: tuple[str, ...] = (),
    topic_ids: tuple[int, ...] = (),
) -> dict[str, object]:
    if not app_token:
        raise WxPusherError("WXPUSHER_APP_TOKEN is required")
    if not uids and not topic_ids:
        raise WxPusherError("WXPUSHER_UIDS or WXPUSHER_TOPIC_IDS is required")

    payload: dict[str, object] = {
        "appToken": app_token,
        "summary": summary,
        "content": content,
        "contentType": 1,
    }
    if uids:
        payload["uids"] = list(uids)
    if topic_ids:
        payload["topicIds"] = list(topic_ids)

    return payload


def send_wxpusher_message(
    *,
    app_token: str,
    summary: str,
    content: str,
    uids: tuple[str, ...],
    topic_ids: tuple[int, ...],
    url: str,
    timeout: int = 10,
) -> WxPusherResult:
    payload = build_wxpusher_payload(
        app_token=app_token,
        summary=summary,
        content=content,
        uids=uids,
        topic_ids=topic_ids,
    )
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
        raise WxPusherError(f"Failed to send WxPusher message: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise WxPusherError("WxPusher returned invalid JSON") from exc

    code = result.get("code")
    message = str(result.get("msg") or result.get("message") or result)
    if code != 1000:
        raise WxPusherError(f"WxPusher send failed: code={code}, message={message}")

    return WxPusherResult(code=code, message=message)
