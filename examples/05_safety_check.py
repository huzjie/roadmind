"""安全校验示例。"""
from roadmind.config.loader import load_config
from roadmind.planning.motion import MotionPlanner
from roadmind.planning.safety import SafetyChecker
from roadmind.core.types import Detection, BoundingBox3D

config = load_config()
motion = MotionPlanner(config.planning)
safety = SafetyChecker(config.planning)

traj = motion.straight()
others = [Detection(box3d=BoundingBox3D(10.0, 0.5, 0, 4, 1.8, 1.5, 0, "car"),
                    velocity=(0.0, 0.0))]
print("是否安全:", safety.is_safe(traj, others))
print("最小距离:", safety.min_distance(traj, others))
