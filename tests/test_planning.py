"""规划模块测试。"""
from roadmind.config.loader import load_config
from roadmind.planning.decision import DecisionMaker
from roadmind.planning.motion import MotionPlanner
from roadmind.planning.safety import SafetyChecker
from roadmind.planning.trajectory import TrajectoryPredictor
from roadmind.core.types import BoundingBox3D, Detection, TrafficLight, SceneGraph


def test_decision_stop():
    dm = DecisionMaker(load_config().planning)
    scene = SceneGraph(lights=[TrafficLight(1, "red")])
    cmd = dm.decide(scene)
    assert cmd.action == "STOP"


def test_decision_default():
    dm = DecisionMaker(load_config().planning)
    cmd = dm.decide(SceneGraph())
    assert cmd.action == "KEEP_LANE"


def test_motion_straight():
    mp = MotionPlanner(load_config().planning)
    traj = mp.straight(target_speed=10.0)
    assert traj.length > 0
    assert traj.waypoints[-1].vx <= 10.0 + 1e-6


def test_motion_stop():
    mp = MotionPlanner(load_config().planning)
    traj = mp.stop()
    assert traj.waypoints[-1].vx == 0.0


def test_safety():
    cfg = load_config().planning
    mp = MotionPlanner(cfg)
    sc = SafetyChecker(cfg)
    traj = mp.straight()
    others = [Detection(box3d=BoundingBox3D(100, 100, 0, 4, 1.8, 1.5, 0, "car"))]
    assert sc.is_safe(traj, others)
