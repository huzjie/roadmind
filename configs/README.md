# 配置示例

- `roadmind.yaml` — 完整示例（本地 transformers 后端）
- `roadmind.mock.yaml` — 离线 Mock（CI / 自检 / 演示）
- `roadmind.ollama.yaml` — Ollama 本地推理
- `roadmind.openai.yaml` — OpenAI 兼容远程端点

用法：

```bash
roadmind --config configs/roadmind.mock.yaml doctor
roadmind --config configs/roadmind.mock.yaml serve
```
