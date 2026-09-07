"""轨迹预测：为动态目标预测未来轨迹。"""
from __future__ import annotations

from typing import List, Optional, Tuple

from roadmind.config.schema import PlanningConfig
from roadmind.core.types import Detection, Trajectory, Waypoint


class TrajectoryPredictor:
    """基于恒定速度 / 恒定加速度模型的轨迹预测。"""

    def __init__(self, config: PlanningConfig) -> None:
        self.config = config

    def predict(self, det: Detection, dt: Optional[float] = None,
                horizon: Optional[float] = None) -> Trajectory:
        """预测单个目标未来轨迹。"""
        dt = dt or self.config.dt
        horizon = horizon or self.config.horizon
        vx, vy = det.velocity or (0.0, 0.0)
        x0 = det.box3d.cx if det.box3d else 0.0
        y0 = det.box3d.cy if det.box3d else 0.0
        steps = int(horizon / dt)
        waypoints = [
            Waypoint(x=x0 + vx * (i * dt), y=y0 + vy * (i * dt), t=i * dt, vx=vx, vy=vy)
            for i in range(steps + 1)
        ]
        return Trajectory(waypoints=waypoints, source="constant-velocity")

    def predict_all(self, detections: List[Detection]) -> List[Trajectory]:
        return [self.predict(d) for d in detections if (d.velocity is not None or d.box3d is not None)]
