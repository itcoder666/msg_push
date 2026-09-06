# msg-push

每天自动获取美元兑人民币汇率，并通过 PushPlus 推送到微信。

## 功能

- 从新浪财经接口获取 USD/CNY 实时汇率
- 通过 PushPlus 发送微信消息
- 支持 GitHub Actions 每天自动运行
- 使用标准 Python `src` 工程结构，便于测试和维护

## 本地运行

建议使用 Python 3.11 或更高版本。

```bash
python -m pip install -e .[dev]
```

只运行程序：

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

## GitHub Actions 自动推送

项目已包含 workflow：[.github/workflows/exchange-rate-push.yml](.github/workflows/exchange-rate-push.yml)。

默认计划：每天北京时间 09:00 执行。

GitHub Actions 的 cron 使用 UTC，因此 workflow 中配置的是：

```yaml
- cron: "0 1 * * *"
```

### 配置 PushPlus Secret

1. 打开 GitHub 仓库页面
2. 进入 **Settings → Secrets and variables → Actions**
3. 点击 **New repository secret**
4. Name 填写：`PUSHPLUS_TOKEN`
5. Secret 填写你的 PushPlus token
6. 保存后，可在 **Actions → Daily Exchange Rate Push → Run workflow** 手动触发一次验证

## 配置项

| 环境变量 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `PUSHPLUS_TOKEN` | 是 | 无 | PushPlus token |
| `SINA_EXCHANGE_URL` | 否 | `https://hq.sinajs.cn/list=fx_susdcny` | 新浪汇率接口 |
| `PUSHPLUS_URL` | 否 | `https://www.pushplus.plus/send` | PushPlus API 地址 |

不要把真实 token 写入代码、README、`.env.example` 或提交到 Git 仓库。

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
