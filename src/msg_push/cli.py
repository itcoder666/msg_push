from __future__ import annotations
from datetime import datetime

from msg_push.config import ConfigError, MissingNotificationChannelError, load_settings
from msg_push.exchange_rate import ExchangeRate, fetch_usdcny_rate
from msg_push.notifiers import NotificationDeliveryError, send_configured_notifications


def build_message(exchange_rate: ExchangeRate) -> str:
    suffix = ""
    if exchange_rate.source_date or exchange_rate.source_time:
        source_at = " ".join(
            part
            for part in [exchange_rate.source_date, exchange_rate.source_time]
            if part
        )
        suffix = f"\n数据时间：{source_at}"
        suffix = suffix + f"\n查询时间 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return f"当前美元兑人民币汇率为：1 USD = {exchange_rate.rate:.4f} CNY{suffix}"


def build_title(exchange_rate: ExchangeRate) -> str:
    return f"汇率:1USD={exchange_rate.rate:.4f}CNY"


def main() -> int:
    try:
        settings = load_settings()
        exchange_rate = fetch_usdcny_rate(settings.exchange_rate_url)
        title = build_title(exchange_rate)
        message = build_message(exchange_rate)
        print(message)

        results = send_configured_notifications(settings, title=title, content=message)
        for result in results:
            print(f"{result.channel}: success")
        return 0
    except MissingNotificationChannelError as exc:
        print(f"配置错误：{exc}")
        return 2
    except NotificationDeliveryError as exc:
        for result in exc.results:
            if result.success:
                print(f"{result.channel}: success")
            else:
                print(f"{result.channel}: failed ({result.error})")
        return 1
    except (ConfigError, RuntimeError, ValueError) as exc:
        print(f"运行失败：{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
