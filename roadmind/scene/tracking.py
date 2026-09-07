"""多目标跟踪（简单 IoU 关联）。"""
from __future__ import annotations

from typing import List

from roadmind.core.types import Detection
from roadmind.perception.fusion import SensorFusion


class ObjectTracker:
    """基于 IoU 的在线目标跟踪，分配 track_id。"""

    def __init__(self, iou_threshold: float = 0.3, max_age: int = 30) -> None:
        self.iou_threshold = iou_threshold
        self.max_age = max_age
        self._tracks: List[Detection] = []
        self._next_id = 0

    def update(self, detections: List[Detection]) -> List[Detection]:
        for det in detections:
            best = None
            best_iou = 0.0
            for track in self._tracks:
                iou = SensorFusion.iou(det, track)
                if iou > best_iou:
                    best_iou = iou
                    best = track
            if best is not None and best_iou >= self.iou_threshold:
                det.track_id = best.track_id
            else:
                det.track_id = self._next_id
                self._next_id += 1
        self._tracks = detections
        return detections
