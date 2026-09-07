"""感知路由。"""
from __future__ import annotations

try:
    from fastapi import APIRouter
except ImportError:  # pragma: no cover
    APIRouter = None  # type: ignore

from roadmind.core.context import RuntimeContext


def make_perception_router(ctx: RuntimeContext):
    if APIRouter is None:  # pragma: no cover
        return None
    router = APIRouter(tags=["perception"])

    @router.post("/perceive")
    def perceive(body: dict) -> dict:
        pipeline = ctx.get("perception")
        image = body.get("image")
        result = pipeline.run(image)
        return {
            "detections": [d.label for d in result.detections],
            "lanes": len(result.lanes),
            "lights": [l.state for l in result.lights],
            "signs": [s.sign_type for s in result.signs],
            "scene_summary": "",
        }

    return router
