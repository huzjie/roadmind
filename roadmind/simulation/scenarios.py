"""预置仿真场景。"""
from __future__ import annotations

from roadmind.simulation.ego import EgoVehicle
from roadmind.simulation.obstacle import Obstacle
from roadmind.simulation.world import World


def free_road() -> tuple:
    """空旷直道。"""
    return World(), EgoVehicle(), []


def leading_car(distance: float = 30.0) -> tuple:
    """前方有静止车辆。"""
    world = World()
    ego = EgoVehicle()
    obstacles = [Obstacle(x=distance, y=0.0)]
    return world, ego, obstacles


def cut_in() -> tuple:
    """侧向切入车辆。"""
    world = World()
    ego = EgoVehicle()
    obstacles = [Obstacle(x=25.0, y=1.75, velocity=(-2.0, -1.0))]
    return world, ego, obstacles
