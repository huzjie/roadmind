"""推理路由。"""
from __future__ import annotations

try:
    from fastapi import APIRouter
except ImportError:  # pragma: no cover
    APIRouter = None  # type: ignore

from roadmind.core.context import RuntimeContext


def make_inference_router(ctx: RuntimeContext):
    if APIRouter is None:  # pragma: no cover
        return None
    router = APIRouter(tags=["inference"])

    @router.post("/generate")
    def generate(body: dict) -> dict:
        engine = ctx.get("engine")
        text = engine.generate(body.get("prompt", ""), image=body.get("image"),
                               system=body.get("system"))
        desc = engine.describe()
        return {"text": text, "backend": desc["backend"], "model": desc["model"]}

    @router.get("/models")
    def models() -> dict:
        return {"models": [c.name for c in ctx.models.list()]}

    return router
