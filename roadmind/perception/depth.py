"""单目深度估计占位模块。"""
from __future__ import annotations

from typing import Any, Optional


class DepthEstimator:
    """单目深度估计（可挂载 MiDaS / Depth Anything）。"""

    def __init__(self, model: str = "depth-anything-small") -> None:
        self.model = model

    def estimate(self, image: Optional[Any] = None) -> Optional[Any]:
        if image is None:
            return None
        return {"model": self.model, "depth_map": None}
