"""core 基础测试。"""
from roadmind.core.types import BoundingBox2D, Detection, Waypoint, Trajectory


def test_bbox2d():
    b = BoundingBox2D(0, 0, 10, 20, "car")
    assert b.width == 10
    assert b.height == 20
    assert b.area == 200


def test_trajectory():
    traj = Trajectory(waypoints=[Waypoint(0, 0, 0), Waypoint(1, 0, 0.5)])
    assert traj.length == 2
    assert traj.duration == 0.5


def test_detection():
    d = Detection(label="pedestrian", confidence=0.9)
    assert d.label == "pedestrian"
