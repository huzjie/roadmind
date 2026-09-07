"""安全校验：碰撞时间 TTC、安全距离。"""
from __future__ import annotations

import math
from typing import List, Optional

from roadmind.config.schema import PlanningConfig
from roadmind.core.types import Detection, Trajectory, Waypoint


class SafetyChecker:
    """对规划轨迹做安全校验。"""

    def __init__(self, config: PlanningConfig) -> None:
        self.config = config

    def time_to_collision(self, ego: Waypoint, other: Detection,
                          other_traj: Optional[Trajectory] = None) -> float:
        """估计与目标的时间到碰撞；无风险返回 inf。"""
        vx, vy = other.velocity or (0.0, 0.0)
        speed = math.hypot(vx, vy)
        ox = other.box3d.cx if other.box3d else 0.0
        oy = other.box3d.cy if other.box3d else 0.0
        dist = math.hypot(ox - ego.x, oy - ego.y)
        if speed <= 1e-3:
            return float("inf") if dist > self.config.safety_margin else 0.0
        return max(0.0, (dist - self.config.safety_margin) / speed)

    def is_safe(self, ego_traj: Trajectory, others: List[Detection],
                other_trajs: Optional[List[Trajectory]] = None) -> bool:
        """整条轨迹是否安全。"""
        if not ego_traj.waypoints:
            return True
        trajs = other_trajs or []
        for i, wp in enumerate(ego_traj.waypoints):
            for j, other in enumerate(others):
                ot = trajs[j] if j < len(trajs) else None
                ttc = self.time_to_collision(wp, other, ot)
                if ttc < 1.0:
                    return False
        return True

    def min_distance(self, ego_traj: Trajectory, others: List[Detection]) -> float:
        """轨迹与目标的最小距离。"""
        if not ego_traj.waypoints:
            return float("inf")
        best = float("inf")
        for wp in ego_traj.waypoints:
            for other in others:
                ox = other.box3d.cx if other.box3d else 0.0
                oy = other.box3d.cy if other.box3d else 0.0
                best = min(best, math.hypot(ox - wp.x, oy - wp.y))
        return best
