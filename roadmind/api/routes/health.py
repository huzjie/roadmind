"""健康检查路由。"""
from __future__ import annotations

try:
    from fastapi import APIRouter
except ImportError:  # pragma: no cover
    APIRouter = None  # type: ignore

if APIRouter is not None:
    router = APIRouter(tags=["health"])
else:  # pragma: no cover
    router = None


if router is not None:
    @router.get("/health")
    def health() -> dict:
        return {"status": "ok", "service": "roadmind"}

    @router.get("/")
    def root() -> dict:
        return {"service": "roadmind", "docs": "/docs"}
