"""规划路由。"""
from __future__ import annotations

try:
    from fastapi import APIRouter
except ImportError:  # pragma: no cover
    APIRouter = None  # type: ignore

from roadmind.core.context import RuntimeContext


def make_planning_router(ctx: RuntimeContext):
    if APIRouter is None:  # pragma: no cover
        return None
    router = APIRouter(tags=["planning"])

    @router.post("/plan")
    def plan(body: dict) -> dict:
        planner = ctx.get("planner")
        result = planner.plan()
        traj = result["trajectory"]
        cmd = result["command"]
        return {
            "action": cmd.action,
            "reason": cmd.reason,
            "safe": result["safe"],
            "scene_summary": result["scene_summary"],
            "waypoints": traj.length,
        }

    return router
