"""评测指标测试。"""
from roadmind.eval.metrics import compute_ade, compute_fde
from roadmind.config.loader import load_config
from roadmind.planning.motion import MotionPlanner


def test_ade_self_zero():
    mp = MotionPlanner(load_config().planning)
    traj = mp.straight()
    assert compute_ade(traj, traj) == 0.0
    assert compute_fde(traj, traj) == 0.0
