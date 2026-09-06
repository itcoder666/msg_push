from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class WeChatWorkResult:
    errcode: int | None
    message: str


class WeChatWorkError(RuntimeError):
    """Raised when the WeChat Work group robot rejects a message."""


def build_wechat_work_payload(content: str) -> dict[str, object]:
    return {
        "msgtype": "text",
        "text": {
            "content": content,
        },
    }


def send_wechat_work_message(
    *,
    webhook_url: str,
    content: str,
    timeout: int = 10,
) -> WeChatWorkResult:
    if not webhook_url:
        raise WeChatWorkError("WECHAT_WORK_WEBHOOK_URL is required")

    body = json.dumps(build_wechat_work_payload(content), ensure_ascii=False).encode(
        "utf-8"
    )
    request = Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            raw_response = response.read().decode("utf-8")
            result = json.loads(raw_response)
    except URLError as exc:
        raise WeChatWorkError(f"Failed to send WeChat Work message: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise WeChatWorkError("WeChat Work returned invalid JSON") from exc

    errcode = result.get("errcode")
    message = str(result.get("errmsg") or result)
    if errcode != 0:
        raise WeChatWorkError(
            f"WeChat Work send failed: errcode={errcode}, message={message}"
        )

    return WeChatWorkResult(errcode=errcode, message=message)
