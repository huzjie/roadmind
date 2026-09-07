"""闭环仿真器：自车 + 障碍物按时间步推进。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from roadmind.simulation.ego import EgoVehicle
from roadmind.simulation.obstacle import Obstacle
from roadmind.simulation.world import World


@dataclass
class SimStep:
    """单步仿真状态。"""

    t: float
    ego: Tuple[float, float, float, float]  # x, y, heading, speed
    obstacles: List[Tuple[float, float]]
    collision: bool
    off_road: bool


class Simulator:
    """执行固定步长的闭环仿真。"""

    def __init__(self, world: World, ego: EgoVehicle, obstacles: List[Obstacle],
                 dt: float = 0.5) -> None:
        self.world = world
        self.ego = ego
        self.obstacles = obstacles
        self.dt = dt
        self.t = 0.0
        self.history: List[SimStep] = []

    def step(self, accel: float = 0.0, steer: float = 0.0) -> SimStep:
        """推进一步，返回状态。"""
        self.ego.step(accel, steer, self.dt)
        for ob in self.obstacles:
            ob.step(self.dt)
        self.t += self.dt
        collision = self._check_collision()
        off_road = not self.world.in_bounds(self.ego.x, self.ego.y)
        state = SimStep(
            t=self.t,
            ego=(self.ego.x, self.ego.y, self.ego.heading, self.ego.speed),
            obstacles=[(o.x, o.y) for o in self.obstacles],
            collision=collision,
            off_road=off_road,
        )
        self.history.append(state)
        return state

    def run(self, steps: int, accel: float = 0.0, steer: float = 0.0) -> List[SimStep]:
        for _ in range(steps):
            st = self.step(accel, steer)
            if st.collision or st.off_road:
                break
        return self.history

    def _check_collision(self) -> bool:
        for ob in self.obstacles:
            if self._rect_overlap(ob):
                return True
        return False

    def _rect_overlap(self, ob: Obstacle) -> bool:
        ex, ey = self.ego.x, self.ego.y
        hx = ob.length / 2.0
        hy = ob.width / 2.0
        return abs(ex - ob.x) <= hx and abs(ey - ob.y) <= hy
