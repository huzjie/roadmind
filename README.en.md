# RoadMind 🚗🧠

**Autonomous Driving Vision-Language Model Inference & Planning Platform**

A production-grade toolkit built around **Qwen-Drive-1.0-4B** (the first vision-language foundation model for autonomous driving, open-sourced by Alibaba Qwen on 2026-09-07), unifying **3D perception + scene VQA + motion planning** into one runnable, servable, evaluable system.

## Highlights

- 🧠 Multi-backend inference (transformers / vLLM / Ollama / OpenAI-compatible / offline Mock) with fallback + caching
- 👁️ Unified 3D perception (detection, BEV, lanes, sensor fusion, tracking)
- 💬 Scene / traffic / risk visual question answering
- 🛣️ Motion planning (trajectory prediction, straight / lane-change / stop, rule+model decision, TTC safety)
- 🖥️ CLI + FastAPI REST + Python SDK
- 📊 Evaluation metrics (ADE / FDE / collision rate)
- 🚀 Docker / Kubernetes / CI, model catalog, examples, docs, tests

## Quick start

```bash
pip install -e .
roadmind doctor                                   # self-check (no GPU)
roadmind --config configs/roadmind.mock.yaml serve --port 8000
```

See [`README.md`](README.md) and [`docs/`](docs/) for full details.

## License

[Apache-2.0](LICENSE)
