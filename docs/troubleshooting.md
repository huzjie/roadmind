# 故障排查

| 现象 | 原因 | 解决 |
|---|---|---|
| `ModuleNotFoundError: torch` | 未装 torch | `pip install -e ".[torch]"` |
| `ModuleNotFoundError: fastapi` | 未装服务依赖 | `pip install -e ".[server]"` |
| 后端全部不可用 | 模型未下载/依赖缺失 | 用 Mock 后端或检查 fallback |
| 401 / 网络错误 | 远程端点配置问题 | 检查 `OPENAI_BASE_URL` / key |
