"""导出轨迹为 SVG 文件。"""
from roadmind.config.loader import load_config
from roadmind.planning.motion import MotionPlanner
from roadmind.tools.visualize import render_trajectory_svg

config = load_config()
mp = MotionPlanner(config.planning)
svg = render_trajectory_svg([mp.lane_change()], title="lane change")
with open("trajectory.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("已导出 trajectory.svg")
