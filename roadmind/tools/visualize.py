"""轨迹 SVG 可视化（纯 stdlib）。"""
from __future__ import annotations

from typing import List, Optional, Tuple

from roadmind.core.types import Trajectory


def render_trajectory_svg(trajectories: List[Trajectory], width: int = 600,
                          height: int = 400, title: str = "trajectory") -> str:
    """把多条轨迹渲染为 SVG 字符串。"""
    xs: List[float] = []
    ys: List[float] = []
    for traj in trajectories:
        for wp in traj.waypoints:
            xs.append(wp.x)
            ys.append(wp.y)
    if not xs:
        xs = [0.0, 1.0]
        ys = [0.0, 1.0]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    pad_x = (max_x - min_x) * 0.1 + 1.0
    pad_y = (max_y - min_y) * 0.1 + 1.0
    min_x -= pad_x
    max_x += pad_x
    min_y -= pad_y
    max_y += pad_y

    def sx(x: float) -> float:
        return (x - min_x) / (max_x - min_x) * width

    def sy(y: float) -> float:
        return height - (y - min_y) / (max_y - min_y) * height

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}" viewBox="0 0 {0} {1}">'.format(width, height),
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="10" y="20" font-family="sans-serif" font-size="14" fill="#333">{0}</text>'.format(title),
    ]
    colors = ["#e60012", "#1a73e8", "#188038", "#f9ab00", "#9334e6"]
    for i, traj in enumerate(trajectories):
        color = colors[i % len(colors)]
        points = " ".join("{0:.1f},{1:.1f}".format(sx(wp.x), sy(wp.y)) for wp in traj.waypoints)
        if points:
            parts.append('<polyline points="{0}" fill="none" stroke="{1}" stroke-width="2"/>'.format(points, color))
    parts.append("</svg>")
    return "".join(parts)
