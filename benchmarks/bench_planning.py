"""规划模块性能基准。"""
import time

from roadmind.config.loader import load_config
from roadmind.planning.motion import MotionPlanner

config = load_config()
mp = MotionPlanner(config.planning)

start = time.perf_counter()
for _ in range(1000):
    mp.straight()
elapsed = time.perf_counter() - start
print(f"1000 次直行规划耗时: {elapsed:.3f}s ({elapsed/10:.3f}ms/次)")
