from __future__ import annotations

from datetime import datetime

from msg_push.config import MissingTokenError, load_settings
from msg_push.exchange_rate import ExchangeRate, fetch_usdcny_rate
from msg_push.pushplus import PushPlusError, send_pushplus_message


def build_message(exchange_rate: ExchangeRate) -> str:
    suffix = ""
    if exchange_rate.source_date or exchange_rate.source_time:
        source_at = " ".join(
            part
            for part in [exchange_rate.source_date, exchange_rate.source_time]
            if part
        )
        suffix = f"\n数据时间：{source_at}"

    return f"当前美元兑人民币汇率为：1 USD = {exchange_rate.rate:.4f} CNY{suffix}"


def build_title() -> str:
    return f"汇率日报 {datetime.now().strftime('%Y-%m-%d')}"


def main() -> int:
    settings = load_settings()

    try:
        exchange_rate = fetch_usdcny_rate(settings.exchange_rate_url)
        message = build_message(exchange_rate)
        print(message)

        send_pushplus_message(
            token=settings.pushplus_token,
            title=build_title(),
            content=message,
            url=settings.pushplus_url,
        )
        print("消息推送成功！")
        return 0
    except MissingTokenError as exc:
        print(f"配置错误：{exc}")
        return 2
    except (RuntimeError, ValueError, PushPlusError) as exc:
        print(f"运行失败：{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
