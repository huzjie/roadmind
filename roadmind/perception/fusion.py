"""多传感器融合模块。"""
from __future__ import annotations

from typing import List

from roadmind.core.types import Detection, PerceptionResult


class SensorFusion:
    """融合相机检测与其它传感器（雷达 / 激光）结果。"""

    def __init__(self, iou_threshold: float = 0.5) -> None:
        self.iou_threshold = iou_threshold

    def fuse(self, results: List[PerceptionResult]) -> PerceptionResult:
        """合并多个感知结果，简单去重（按 label）。"""
        merged = PerceptionResult()
        seen = set()
        for res in results:
            for det in res.detections:
                if det.label in seen:
                    continue
                seen.add(det.label)
                merged.detections.append(det)
            merged.lanes.extend(res.lanes)
            merged.lights.extend(res.lights)
            merged.signs.extend(res.signs)
        return merged

    @staticmethod
    def iou(a: Detection, b: Detection) -> float:
        if a.box2d is None or b.box2d is None:
            return 0.0
        x1 = max(a.box2d.x1, b.box2d.x1)
        y1 = max(a.box2d.y1, b.box2d.y1)
        x2 = min(a.box2d.x2, b.box2d.x2)
        y2 = min(a.box2d.y2, b.box2d.y2)
        inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
        union = a.box2d.area + b.box2d.area - inter
        return inter / union if union > 0 else 0.0
