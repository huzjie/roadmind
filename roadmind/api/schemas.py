"""API 请求 / 响应模型（pydantic）。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover
    BaseModel = object  # type: ignore
    Field = lambda *a, **k: None  # type: ignore


class GenerateRequest(BaseModel if BaseModel is not object else object):
    prompt: str = ""
    image: Optional[str] = None
    system: Optional[str] = None


class GenerateResponse(BaseModel if BaseModel is not object else object):
    text: str
    backend: str = ""
    model: str = ""


class PerceiveResponse(BaseModel if BaseModel is not object else object):
    detections: List[str] = []
    lanes: int = 0
    lights: List[str] = []
    signs: List[str] = []
    scene_summary: str = ""


class PlanResponse(BaseModel if BaseModel is not object else object):
    action: str = "KEEP_LANE"
    reason: str = ""
    safe: bool = True
    scene_summary: str = ""
    waypoints: int = 0
