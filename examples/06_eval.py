"""评测指标示例。"""
from roadmind.eval.metrics import compute_ade, compute_fde
from roadmind.planning.motion import MotionPlanner
from roadmind.config.loader import load_config

config = load_config()
motion = MotionPlanner(config.planning)
pred = motion.straight(target_speed=10.0)
gt = motion.straight(target_speed=9.0)

print("ADE:", round(compute_ade(pred, gt), 4))
print("FDE:", round(compute_fde(pred, gt), 4))
