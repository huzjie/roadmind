"""高层决策：把场景 + 模型指令转换为驾驶指令。"""
from __future__ import annotations

from typing import List, Optional

from roadmind.config.schema import PlanningConfig
from roadmind.core.types import DrivingCommand, SceneGraph, TrafficLight
from roadmind.core.logging import get_logger

logger = get_logger("roadmind.planning")


class DecisionMaker:
    """规则 + 模型指令融合的决策器。"""

    def __init__(self, config: PlanningConfig) -> None:
        self.config = config

    def decide(self, scene: Optional[SceneGraph] = None,
               model_command: Optional[str] = None) -> DrivingCommand:
        """返回高层驾驶指令。"""
        cmd = model_command or ""

        # 1. 交通灯硬约束优先
        red = self._has_red_light(scene)
        if red:
            return DrivingCommand(action="STOP", reason="红灯", target_speed=0.0)

        # 2. 模型指令分类
        action = self._classify(cmd)
        if action == "STOP":
            return DrivingCommand(action="STOP", reason="模型判断需停车", target_speed=0.0)
        if action == "SLOW_DOWN":
            return DrivingCommand(action="SLOW_DOWN", reason="存在风险目标",
                                  target_speed=self.config.target_speed * 0.4)
        if action in ("TURN_LEFT", "TURN_RIGHT", "CHANGE_LANE"):
            return DrivingCommand(action=action, reason="模型指令",
                                  target_speed=self.config.target_speed * 0.6)

        # 3. 默认保持车道
        return DrivingCommand(action="KEEP_LANE", reason="默认",
                              target_speed=self.config.target_speed)

    @staticmethod
    def _has_red_light(scene: Optional[SceneGraph]) -> bool:
        if scene is None:
            return False
        return any(l.state == "red" for l in scene.lights)

    @staticmethod
    def _classify(cmd: str) -> str:
        upper = (cmd or "").upper()
        for action in ("STOP", "SLOW_DOWN", "TURN_LEFT", "TURN_RIGHT", "CHANGE_LANE", "KEEP_LANE"):
            if action in upper:
                return action
        return "KEEP_LANE"

    @staticmethod
    def visible_lights(scene: Optional[SceneGraph]) -> List[TrafficLight]:
        if scene is None:
            return []
        return scene.lights
