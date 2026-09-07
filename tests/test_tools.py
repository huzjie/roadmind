"""工具模块测试。"""
from roadmind.config.loader import load_config
from roadmind.planning.motion import MotionPlanner
from roadmind.tools.visualize import render_trajectory_svg
from roadmind.tools.aggregate import aggregate_results


def test_render_svg():
    mp = MotionPlanner(load_config().planning)
    svg = render_trajectory_svg([mp.straight()])
    assert "<svg" in svg


def test_aggregate():
    out = aggregate_results([
        {"safe": True, "command": {"action": "KEEP_LANE"}},
        {"safe": False, "command": {"action": "STOP"}},
    ])
    assert out["total"] == 2
    assert out["safe_rate"] == 0.5
