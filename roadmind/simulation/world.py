"""仿真世界：车道边界与目标集合。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class World:
    """简化的 2D 道路世界。"""

    lane_width: float = 3.5
    road_length: float = 200.0
    obstacles: list = field(default_factory=list)
    lanes: int = 2

    @property
    def road_half_width(self) -> float:
        return self.lane_width * self.lanes / 2.0

    def in_bounds(self, x: float, y: float) -> bool:
        return -self.road_half_width <= y <= self.road_half_width and 0 <= x <= self.road_length
