"""自车运动学模型。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EgoVehicle:
    """简单自行车运动学模型。"""

    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0
    speed: float = 0.0
    wheelbase: float = 2.7
    max_accel: float = 3.0
    max_steer: float = 0.6

    def step(self, accel: float, steer: float, dt: float) -> None:
        """执行一步控制。"""
        accel = max(-self.max_accel, min(self.max_accel, accel))
        steer = max(-self.max_steer, min(self.max_steer, steer))
        self.speed = max(0.0, self.speed + accel * dt)
        self.heading += (self.speed / self.wheelbase) * steer * dt
        self.x += self.speed * dt * self._cos(self.heading)
        self.y += self.speed * dt * self._sin(self.heading)

    @staticmethod
    def _cos(a: float) -> float:
        import math
        return math.cos(a)

    @staticmethod
    def _sin(a: float) -> float:
        import math
        return math.sin(a)
