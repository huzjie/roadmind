"""静态 / 动态障碍物。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Obstacle:
    """障碍物（静态或匀速运动）。"""

    x: float
    y: float
    length: float = 4.0
    width: float = 1.8
    velocity: Optional[Tuple[float, float]] = None

    def step(self, dt: float) -> None:
        if self.velocity is not None:
            self.x += self.velocity[0] * dt
            self.y += self.velocity[1] * dt

    def corners(self) -> list:
        """返回四角坐标。"""
        hx = self.length / 2.0
        hy = self.width / 2.0
        return [
            (self.x - hx, self.y - hy),
            (self.x + hx, self.y - hy),
            (self.x + hx, self.y + hy),
            (self.x - hx, self.y + hy),
        ]
