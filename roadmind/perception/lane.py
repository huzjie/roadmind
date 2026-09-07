"""车道线检测模块。"""
from __future__ import annotations

from typing import List, Optional, Tuple

from roadmind.core.types import Lane


class LaneDetector:
    """车道线检测：规则化分段拟合（真实实现可挂载 LaneNet/CLRNet）。"""

    def __init__(self, conf_threshold: float = 0.3) -> None:
        self.conf_threshold = conf_threshold

    def detect(self, image: Optional[object] = None) -> List[Lane]:
        if image is None:
            return []
        return []

    @staticmethod
    def fit_polyline(points: List[Tuple[float, float]], lane_id: int = 0) -> Lane:
        """由点集构造车道实例。"""
        return Lane(lane_id=lane_id, polyline=points, lane_type="dashed", confidence=1.0)
