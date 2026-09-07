# FAQ

**Q：没有 GPU 能跑吗？**
A：能。使用 Mock 后端（`configs/roadmind.mock.yaml`）可离线跑通全链路。

**Q：如何接入真实模型？**
A：安装 `roadmind[torch]` 后，将 `inference.model.name` 指向 HF 模型，`backend` 设为 transformers/vllm。

**Q：如何对接 OpenAI 兼容端点？**
A：设 `backend: openai`，并配置 `OPENAI_BASE_URL` / `OPENAI_API_KEY` 环境变量。
