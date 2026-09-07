"""规划 / 预测评测指标。"""
from __future__ import annotations

import math
from typing import List

from roadmind.core.types import Trajectory


def _pairwise(pred: Trajectory, gt: Trajectory) -> List[float]:
    """逐点欧氏距离。"""
    n = min(pred.length, gt.length)
    dists = []
    for i in range(n):
        a = pred.waypoints[i]
        b = gt.waypoints[i]
        dists.append(math.hypot(a.x - b.x, a.y - b.y))
    return dists


def compute_ade(pred: Trajectory, gt: Trajectory) -> float:
    """平均位移误差。"""
    dists = _pairwise(pred, gt)
    return sum(dists) / len(dists) if dists else float("inf")


def compute_fde(pred: Trajectory, gt: Trajectory) -> float:
    """终点位移误差。"""
    if pred.length == 0 or gt.length == 0:
        return float("inf")
    a = pred.waypoints[-1]
    b = gt.waypoints[-1]
    return math.hypot(a.x - b.x, a.y - b.y)


def collision_rate(trajs: List[Trajectory], threshold: float = 0.5) -> float:
    """粗略碰撞率（轨迹终点两两距离 < 阈值判定为碰撞）。"""
    if len(trajs) < 2:
        return 0.0
    coll = 0
    total = 0
    for i in range(len(trajs)):
        for j in range(i + 1, len(trajs)):
            if trajs[i].length == 0 or trajs[j].length == 0:
                continue
            a = trajs[i].waypoints[-1]
            b = trajs[j].waypoints[-1]
            total += 1
            if math.hypot(a.x - b.x, a.y - b.y) < threshold:
                coll += 1
    return coll / total if total else 0.0
