"""几何工具。"""
from __future__ import annotations

import math
from typing import Tuple


def distance_2d(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """二维欧氏距离。"""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def heading_angle(dx: float, dy: float) -> float:
    """由位移向量计算航向角（弧度）。"""
    return math.atan2(dy, dx)


def normalize_angle(angle: float) -> float:
    """归一化角度到 [-pi, pi]。"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle
