# 架构设计

RoadMind 采用分层架构：

```
┌─────────────── CLI ───────────────┐
│  doctor / infer / perceive / plan / serve / list  │
└───────────────┬───────────────────┘
                │
┌───────────────▼───────────────────┐
│          REST API (FastAPI)        │
│  /v1/health /generate /perceive /plan  │
└───────────────┬───────────────────┘
                │
┌───────────────▼───────────────────┐
│         Application Layer          │
│  Perception → VQA → Planning       │
└───────────────┬───────────────────┘
                │
┌───────────────▼───────────────────┐
│       Inference Engine (统一)       │
│  transformers / vLLM / Ollama / OpenAI / Mock │
└────────────────────────────────────┘
```

## 模块职责

| 模块 | 职责 |
|---|---|
| `inference` | 多后端推理，统一 generate 接口，回退与缓存 |
| `perception` | 3D 检测、BEV、车道线、融合 |
| `vqa` | 场景 / 交通 / 风险问答 |
| `scene` | 场景图、交通要素、跟踪 |
| `planning` | 轨迹预测、运动规划、决策、安全校验 |
| `eval` | ADE/FDE/碰撞率等指标 |
| `api` | FastAPI 服务 |
| `sdk` | Python 客户端 |
| `observability` | 指标 / 追踪 |
