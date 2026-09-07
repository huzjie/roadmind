# RoadMind 🚗🧠

**自动驾驶视觉语言模型推理与规划平台**

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF.svg)](.github/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](deploy/docker/Dockerfile)

</div>

> 围绕 **2026-09-07 阿里千问开源的「首个面向自动驾驶的视觉语言基础模型」Qwen-Drive-1.0-4B** 构建的工程化平台：统一 **3D 感知 + 场景视觉问答 + 运动规划**，让「自动驾驶视觉语言模型」真正落地为可运行、可服务化、可评测的生产级工具。

---

## ✨ 这是什么

RoadMind 不是一篇文章、一个话题，而是一套**填写配置即可直接运行**的完整项目：

- 🧠 **多后端推理引擎**：transformers / vLLM / Ollama / OpenAI 兼容 / 离线 Mock 五种后端，统一 `generate()` 接口，支持失败回退 + 响应缓存
- 👁️ **统一 3D 感知**：目标检测、BEV 特征、车道线、多传感器融合、多目标跟踪
- 💬 **场景视觉问答**：场景问答、交通要素（信号灯/标志）问答、驾驶风险问答
- 🛣️ **运动规划**：轨迹预测（恒速/恒加速）、运动规划（直行/变道/停车，五次多项式横向）、规则+模型融合决策、TTC 安全校验
- 🖥️ **三入口**：CLI / OpenAI 风格 REST API（FastAPI）/ Python SDK
- 📊 **评测**：ADE / FDE / 碰撞率等指标 + 基准定义
- 🚀 **完整工程**：Docker 多阶段构建、K8s 部署清单、GitHub Actions CI、模型目录、示例、文档、测试

**无需 GPU 也能跑**：内置离线 Mock 后端，`roadmind doctor` 自检 + 全链路冒烟在普通笔记本即可通过。

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/huzjie/roadmind.git
cd roadmind
pip install -e .
```

### 自检（无需 GPU）

```bash
roadmind doctor
# 输出当前后端、模型、Mock 冒烟结果
```

### 离线跑通全链路

```bash
roadmind --config configs/roadmind.mock.yaml doctor
roadmind --config configs/roadmind.mock.yaml plan
```

### 启动 HTTP 服务

```bash
roadmind --config configs/roadmind.mock.yaml serve --port 8000
# 浏览器打开 http://127.0.0.1:8000/docs 查看 Swagger UI
```

### Python SDK

```python
from roadmind.sdk.client import RoadMindClient

client = RoadMindClient("http://127.0.0.1:8000/v1")
client.health()
client.generate("前方红灯，请给指令。")
client.plan()
```

---

## 🧩 架构

```
┌─────────────── CLI ───────────────┐
│ doctor / infer / perceive / plan / serve / list │
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

| 模块 | 职责 |
|---|---|
| `roadmind/inference` | 多后端推理、回退、缓存、提示词 |
| `roadmind/perception` | 3D 检测、BEV、车道线、融合、流水线 |
| `roadmind/vqa` | 场景 / 交通 / 风险问答 |
| `roadmind/scene` | 场景图、交通要素、跟踪 |
| `roadmind/planning` | 轨迹预测、运动规划、决策、安全 |
| `roadmind/eval` | 评测指标与执行器 |
| `roadmind/api` | FastAPI 服务 |
| `roadmind/sdk` | Python 客户端 |
| `roadmind/observability` | 指标 / 追踪 / Prometheus |

---

## ⚙️ 配置

完整字段见 [`roadmind/config/defaults.yaml`](roadmind/config/defaults.yaml)，示例见 [`configs/`](configs/)：

| 配置 | 说明 |
|---|---|
| `roadmind.yaml` | 完整示例（transformers 后端） |
| `roadmind.mock.yaml` | 离线 Mock（CI / 演示） |
| `roadmind.ollama.yaml` | Ollama 本地推理 |
| `roadmind.openai.yaml` | OpenAI 兼容远程端点 |

关键字段：

| 字段 | 说明 | 默认 |
|---|---|---|
| `inference.model.name` | 模型名称 | `Qwen/Qwen-Drive-1.0-4B` |
| `inference.model.backend` | 推理后端 | `transformers` |
| `inference.fallback_backends` | 回退后端链 | `[mock]` |
| `planning.horizon` | 规划时域（s） | `6.0` |
| `planning.target_speed` | 目标车速（m/s） | `10.0` |
| `server.port` | 服务端口 | `8000` |

---

## 🔌 支持的模型

默认接入 **Qwen-Drive-1.0-4B**（首个面向自动驾驶的视觉语言基础模型，统一 3D 感知与视觉问答并扩展到运动规划），模型注册卡见 [`models/`](models/)：

| 模型 | 家族 | 任务 | 后端 |
|---|---|---|---|
| Qwen/Qwen-Drive-1.0-4B | Qwen-Drive | 自动驾驶 | transformers |
| Qwen/Qwen3.8-27B | Qwen3.8 | 多模态 VQA | vllm |
| deepseek-ai/DeepSeek-V4-Flash-Vision-Exp | DeepSeek | 视觉 + FP8 | transformers |
| XHToken/Spark-X2.5-4B | Spark | 端侧百万上下文 | ollama |
| Qwen/Qwen3.8-Flash-Next | Qwen3.8 | 多模态快速 | vllm |
| google/timesfm-3.0-pytorch | TimesFM | 时间序列 | transformers |

---

## 🧪 测试与质量

```bash
pip install -e ".[dev]"
pytest -q          # 全部单测
ruff check roadmind  # 代码风格
```

质量基线：多后端推理 + 感知 + 规划 + 评测 + 可观测 + Docker 多阶段 + K8s + 多 Python 版本 CI。

---

## 📚 文档

完整文档见 [`docs/`](docs/)：

- [快速开始](docs/quickstart.md) · [架构设计](docs/architecture.md) · [配置说明](docs/configuration.md)
- [推理后端](docs/backends.md) · [感知模块](docs/perception.md) · [规划模块](docs/planning.md)
- [REST API](docs/api.md) · [Python SDK](docs/sdk.md) · [评测](docs/evaluation.md) · [部署](docs/deployment.md) · [FAQ](docs/faq.md)

示例脚本见 [`examples/`](examples/)，基准见 [`benchmarks/`](benchmarks/)。

---

## 📄 License

[Apache-2.0](LICENSE)

> ⚠️ 本项目仅供研究与工程参考，**不构成任何自动驾驶安全认证**。真实道路部署需满足相应法规与安全标准。
