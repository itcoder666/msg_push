from msg_push.wechat_work import build_wechat_work_payload


def test_build_wechat_work_payload_uses_text_message() -> None:
    payload = build_wechat_work_payload("汇率日报\n当前汇率")

    assert payload == {
        "msgtype": "text",
        "text": {
            "content": "汇率日报\n当前汇率",
        },
    }
