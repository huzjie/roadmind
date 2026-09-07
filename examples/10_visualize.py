"""轨迹可视化示例。"""
from roadmind.config.loader import load_config
from roadmind.planning.motion import MotionPlanner
from roadmind.tools.visualize import render_trajectory_svg

config = load_config()
mp = MotionPlanner(config.planning)
trajs = [mp.straight(), mp.lane_change()]
svg = render_trajectory_svg(trajs, title="planning trajectories")
print(svg[:200], "...")
