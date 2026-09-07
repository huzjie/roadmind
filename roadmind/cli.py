"""命令行入口。"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from roadmind.config.loader import load_config
from roadmind.core.logging import setup_logging
from roadmind.version import __version__


def _build_context(args):
    config = load_config(args.config)
    setup_logging(config.app.log_level, getattr(args, "verbose", False))

    from roadmind.core.context import RuntimeContext
    from roadmind.core.registry import BackendRegistry
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
        name=config.inference.model.name, family="Qwen-Drive",
        task="autonomous-driving", backend=config.inference.model.backend,
        parameter_billions=4.0, context_length=32768, license="Apache-2.0",
        tags=["autonomous-driving", "vlm"],
    ))
    from roadmind.inference.engine import InferenceEngine
    engine = InferenceEngine(config.inference, ctx.backends)
    ctx.set("engine", engine)
    return ctx


def cmd_doctor(args) -> int:
    """自检：后端可用性 + 模型目录。"""
    ctx = _build_context(args)
    engine = ctx.get("engine")
    print("RoadMind doctor")
    print("  version:", __version__)
    print("  模型:", ctx.config.inference.model.name)
    print("  可用后端:", ", ".join(ctx.backends.names()))
    try:
        desc = engine.describe()
        print("  当前后端:", desc["backend"])
    except Exception as exc:  # noqa: BLE001
        print("  后端加载失败:", exc)
        return 1
    print("  Mock 冒烟:", engine.backend().generate("规划路线"))
    return 0


def cmd_infer(args) -> int:
    ctx = _build_context(args)
    engine = ctx.get("engine")
    out = engine.generate(args.prompt, system=args.system)
    print(out)
    return 0


def cmd_perceive(args) -> int:
    ctx = _build_context(args)
    from roadmind.perception.pipeline import PerceptionPipeline
    pipeline = PerceptionPipeline(ctx.config.perception, ctx.get("engine"))
    result = pipeline.run(None)
    print("检测目标:", [d.label for d in result.detections])
    return 0


def cmd_plan(args) -> int:
    ctx = _build_context(args)
    from roadmind.planning.planner import Planner
    planner = Planner(ctx.config.planning, ctx.get("engine"))
    result = planner.plan()
    print("指令:", result["command"].action, "|", result["command"].reason)
    print("安全:", result["safe"], "| 航点:", result["trajectory"].length)
    return 0


def cmd_serve(args) -> int:
    ctx = _build_context(args)
    from roadmind.api.app import create_app
    app = create_app(ctx.config)
    try:
        import uvicorn
    except ImportError:
        print("需要 uvicorn：pip install roadmind[server]")
        return 1
    uvicorn.run(app, host=ctx.config.server.host, port=args.port or ctx.config.server.port)
    return 0


def cmd_list(args) -> int:
    ctx = _build_context(args)
    for card in ctx.models.list():
        print(card.name, "|", card.backend, "|", card.task)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="roadmind", description="自动驾驶视觉语言模型平台")
    p.add_argument("--config", default=None, help="配置文件路径（YAML）")
    p.add_argument("--verbose", action="store_true", help="调试日志")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("doctor", help="自检")
    sp.set_defaults(func=cmd_doctor)

    sp = sub.add_parser("infer", help="文本推理")
    sp.add_argument("prompt")
    sp.add_argument("--system", default=None)
    sp.set_defaults(func=cmd_infer)

    sp = sub.add_parser("perceive", help="运行感知")
    sp.set_defaults(func=cmd_perceive)

    sp = sub.add_parser("plan", help="运行规划")
    sp.set_defaults(func=cmd_plan)

    sp = sub.add_parser("serve", help="启动 HTTP 服务")
    sp.add_argument("--port", type=int, default=None)
    sp.set_defaults(func=cmd_serve)

    sp = sub.add_parser("list", help="列出模型")
    sp.set_defaults(func=cmd_list)

    return p


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
