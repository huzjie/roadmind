"""FastAPI 应用工厂。"""
from __future__ import annotations

from typing import Any, Dict, Optional

from roadmind.config.schema import AppConfig
from roadmind.core.context import RuntimeContext
from roadmind.core.logging import get_logger
from roadmind.inference.engine import InferenceEngine
from roadmind.observability.metrics import Metrics
from roadmind.planning.planner import Planner
from roadmind.perception.pipeline import PerceptionPipeline

logger = get_logger("roadmind.api")


def build_runtime(config: AppConfig) -> RuntimeContext:
    """由配置构建运行时上下文（模型目录 + 后端注册）。"""
    from roadmind.core.context import RuntimeContext
    from roadmind.core.registry import BackendRegistry, ModelRegistry
    from roadmind.inference.backends.mock_backend import MockBackend
    from roadmind.inference.backends.ollama_backend import OllamaBackend
    from roadmind.inference.backends.openai_backend import OpenAICompatibleBackend
    from roadmind.inference.backends.transformers_backend import TransformersBackend
    from roadmind.inference.backends.vllm_backend import VLLMBackend

    ctx = RuntimeContext(config=config)
    ctx.backends.register("transformers", TransformersBackend)
    ctx.backends.register("vllm", VLLMBackend)
    ctx.backends.register("ollama", OllamaBackend)
    ctx.backends.register("openai", OpenAICompatibleBackend)
    ctx.backends.register("mock", MockBackend)

    from roadmind.core.types import ModelCard
    ctx.models.add(ModelCard(
        name=config.inference.model.name,
        family="Qwen-Drive",
        task="autonomous-driving",
        backend=config.inference.model.backend,
        parameter_billions=4.0,
        context_length=32768,
        license="Apache-2.0",
        tags=["autonomous-driving", "vlm", "3d-perception", "motion-planning"],
    ))
    return ctx


def create_app(config: Optional[AppConfig] = None) -> Any:
    """创建 FastAPI 应用。"""
    try:
        from fastapi import FastAPI
    except ImportError as exc:
        raise ImportError("需要 fastapi：pip install roadmind[server]") from exc

    cfg = config or AppConfig()
    ctx = build_runtime(cfg)
    engine = InferenceEngine(cfg.inference, ctx.backends)
    metrics = Metrics()
    perception = PerceptionPipeline(cfg.perception, engine)
    planner = Planner(cfg.planning, engine)

    app = FastAPI(title="RoadMind", version="1.0.0",
                  description="自动驾驶视觉语言模型推理与规划平台")

    ctx.set("engine", engine)
    ctx.set("metrics", metrics)
    ctx.set("perception", perception)
    ctx.set("planner", planner)

    from roadmind.api.routes.health import router as health_router
    from roadmind.api.routes.inference import make_inference_router
    from roadmind.api.routes.perception import make_perception_router
    from roadmind.api.routes.planning import make_planning_router

    prefix = cfg.server.api_prefix.rstrip("/")
    app.include_router(health_router, prefix=prefix)
    app.include_router(make_inference_router(ctx), prefix=prefix)
    app.include_router(make_perception_router(ctx), prefix=prefix)
    app.include_router(make_planning_router(ctx), prefix=prefix)
    return app
