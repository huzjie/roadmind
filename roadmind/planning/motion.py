"""运动规划：生成自车行驶轨迹。"""
from __future__ import annotations

import math
from typing import List, Optional

from roadmind.config.schema import PlanningConfig
from roadmind.core.types import Trajectory, Waypoint


class MotionPlanner:
    """生成平滑的横向 / 纵向轨迹。"""

    def __init__(self, config: PlanningConfig) -> None:
        self.config = config

    def straight(self, target_speed: Optional[float] = None,
                 accel: float = 2.0) -> Trajectory:
        """直行轨迹（恒加速到目标速度）。"""
        v_target = target_speed or self.config.target_speed
        v_target = min(v_target, self.config.max_speed)
        dt = self.config.dt
        horizon = self.config.horizon
        steps = int(horizon / dt)
        waypoints: List[Waypoint] = []
        x = 0.0
        v = 0.0
        for i in range(steps + 1):
            v = min(v + accel * dt, v_target)
            x += v * dt
            waypoints.append(Waypoint(x=x, y=0.0, t=i * dt, vx=v))
        return Trajectory(waypoints=waypoints, source="motion.straight")

    def lane_change(self, target_lane_offset: float = 3.5,
                    target_speed: Optional[float] = None) -> Trajectory:
        """变道轨迹（横向用五次多项式）。"""
        v_target = target_speed or self.config.target_speed
        dt = self.config.dt
        horizon = self.config.horizon
        steps = int(horizon / dt)
        waypoints: List[Waypoint] = []
        for i in range(steps + 1):
            t = i * dt
            s = t / horizon
            lateral = target_lane_offset * (10 * s ** 3 - 15 * s ** 4 + 6 * s ** 5)
            longitudinal = v_target * t
            waypoints.append(Waypoint(x=longitudinal, y=lateral, t=t, vx=v_target))
        return Trajectory(waypoints=waypoints, source="motion.lane_change")

    def stop(self, decel: float = 3.0) -> Trajectory:
        """停车轨迹（匀速减速）。"""
        dt = self.config.dt
        horizon = self.config.horizon
        steps = int(horizon / dt)
        waypoints: List[Waypoint] = []
        v = self.config.target_speed
        x = 0.0
        for i in range(steps + 1):
            v = max(0.0, v - decel * dt)
            x += v * dt
            waypoints.append(Waypoint(x=x, y=0.0, t=i * dt, vx=v))
        return Trajectory(waypoints=waypoints, source="motion.stop")

    @staticmethod
    def distance(waypoints: List[Waypoint]) -> float:
        """累计路径长度。"""
        total = 0.0
        for a, b in zip(waypoints, waypoints[1:]):
            total += math.hypot(b.x - a.x, b.y - a.y)
        return total
