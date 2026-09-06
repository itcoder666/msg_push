# msg-push

每天自动获取美元兑人民币汇率，并通过已配置的推送渠道发送通知。

当前支持 3 个渠道：

- PushPlus
- 企业微信群机器人
- WxPusher

只要配置了某个渠道需要的环境变量，程序就会向该渠道发送消息；配置多个渠道时会同时发送到多个渠道。

## 功能

- 从新浪财经接口获取 USD/CNY 实时汇率
- 支持 PushPlus、企业微信群机器人、WxPusher 三种推送渠道
- 支持 GitHub Actions 每天自动运行
- 使用标准 Python `src` 工程结构，便于测试和维护

## 本地运行

建议使用 Python 3.11 或更高版本。

```bash
python -m pip install -e .[dev]
```

配置至少一个推送渠道后运行：

```bash
PUSHPLUS_TOKEN=你的_pushplus_token python -m msg_push
```

也可以使用安装后的命令：

```bash
PUSHPLUS_TOKEN=你的_pushplus_token exchange-rate-push
```

> Windows PowerShell 示例：
>
> ```powershell
> $env:PUSHPLUS_TOKEN="你的_pushplus_token"
> python -m msg_push
> ```

## 推送渠道配置

### PushPlus

配置 `PUSHPLUS_TOKEN` 即启用 PushPlus。

```bash
PUSHPLUS_TOKEN=你的_pushplus_token
```

#### 一对多群组推送

PushPlus 支持一对多群组消息：在 PushPlus 后台创建群组后，拿到群组编码，并通过 `PUSHPLUS_TOPIC` 配置即可向群组内所有成员推送。

```bash
PUSHPLUS_TOKEN=你的_pushplus_token
PUSHPLUS_TOPIC=你的群组编码
```

- 只配置 `PUSHPLUS_TOKEN` 时，默认一对一推送到你自己的微信
- 同时配置 `PUSHPLUS_TOPIC` 时，消息会发送到对应群组（一对多）

### 企业微信群机器人

配置 `WECHAT_WORK_WEBHOOK_URL` 即启用企业微信群机器人。

```bash
WECHAT_WORK_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的_key
```

获取方式：企业微信群 → 群机器人 → 添加机器人 → 复制 webhook 地址。

### WxPusher

WxPusher 需要配置 `WXPUSHER_APP_TOKEN`，并且至少配置一种接收人：`WXPUSHER_UIDS` 或 `WXPUSHER_TOPIC_IDS`。

```bash
WXPUSHER_APP_TOKEN=你的_wxpusher_app_token
WXPUSHER_UIDS=UID_xxx,UID_yyy
WXPUSHER_TOPIC_IDS=100,200
```

说明：

- `WXPUSHER_UIDS`：多个 UID 用英文逗号分隔
- `WXPUSHER_TOPIC_IDS`：多个 Topic ID 用英文逗号分隔，必须是数字
- UID 和 Topic 可以同时配置，程序会一起传给 WxPusher

## GitHub Actions 自动推送

项目已包含 workflow：[.github/workflows/exchange-rate-push.yml](.github/workflows/exchange-rate-push.yml)。

默认计划：每天北京时间 09:00 执行。

GitHub Actions 的 cron 使用 UTC，因此 workflow 中配置的是：

```yaml
- cron: "0 1 * * *"
```

### 配置 GitHub Secrets

1. 打开 GitHub 仓库页面
2. 进入 **Settings → Secrets and variables → Actions**
3. 点击 **New repository secret**
4. 按需添加下面的 secrets
5. 保存后，可在 **Actions → Daily Exchange Rate Push → Run workflow** 手动触发一次验证

| Secret | 是否必填 | 启用渠道 | 说明 |
| --- | --- | --- | --- |
| `PUSHPLUS_TOKEN` | 否 | PushPlus | 配置后启用 PushPlus |
| `PUSHPLUS_TOPIC` | 否 | PushPlus | 群组编码，配置后 PushPlus 一对多推送 |
| `WECHAT_WORK_WEBHOOK_URL` | 否 | 企业微信群机器人 | 配置后启用企业微信群机器人 |
| `WXPUSHER_APP_TOKEN` | 否 | WxPusher | WxPusher app token |
| `WXPUSHER_UIDS` | 否 | WxPusher | 多个 UID 用英文逗号分隔 |
| `WXPUSHER_TOPIC_IDS` | 否 | WxPusher | 多个 Topic ID 用英文逗号分隔 |

至少需要配置一个完整渠道，否则程序会返回配置错误。

## 完整环境变量

| 环境变量 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `PUSHPLUS_TOKEN` | 否 | 无 | 配置后启用 PushPlus |
| `PUSHPLUS_TOPIC` | 否 | 无 | PushPlus 群组编码，用于一对多推送 |
| `WECHAT_WORK_WEBHOOK_URL` | 否 | 无 | 配置后启用企业微信群机器人 |
| `WXPUSHER_APP_TOKEN` | 否 | 无 | WxPusher app token |
| `WXPUSHER_UIDS` | 否 | 无 | WxPusher UID 列表，英文逗号分隔 |
| `WXPUSHER_TOPIC_IDS` | 否 | 无 | WxPusher Topic ID 列表，英文逗号分隔 |
| `SINA_EXCHANGE_URL` | 否 | `https://hq.sinajs.cn/list=fx_susdcny` | 新浪汇率接口 |
| `PUSHPLUS_URL` | 否 | `https://www.pushplus.plus/send` | PushPlus API 地址 |
| `WXPUSHER_URL` | 否 | `https://wxpusher.zjiecode.com/api/send/message` | WxPusher API 地址 |

不要把真实 token、webhook URL 写入代码、README、`.env.example` 或提交到 Git 仓库。

## 开发命令

运行测试：

```bash
pytest
```

运行静态检查：

```bash
ruff check .
```

## 目录结构

```text
.github/workflows/         GitHub Actions 定时任务
src/msg_push/              应用源码
tests/                     单元测试
pyproject.toml             Python 工程配置
CLAUDE.md                  AI 协作规范
```
