"""统一规划器：感知 -> 决策 -> 轨迹 -> 安全校验。"""
from __future__ import annotations

from typing import List, Optional

from roadmind.config.schema import PlanningConfig
from roadmind.core.logging import get_logger
from roadmind.core.types import DrivingCommand, PerceptionResult, SceneGraph, Trajectory
from roadmind.inference.engine import InferenceEngine
from roadmind.inference.prompts import SYSTEM_PLANNING, classify_action, planning_prompt
from roadmind.planning.decision import DecisionMaker
from roadmind.planning.motion import MotionPlanner
from roadmind.planning.safety import SafetyChecker
from roadmind.planning.trajectory import TrajectoryPredictor
from roadmind.scene.graph import SceneGraphBuilder

logger = get_logger("roadmind.planning")


class Planner:
    """端到端规划入口。"""

    def __init__(self, config: PlanningConfig, engine: InferenceEngine) -> None:
        self.config = config
        self.engine = engine
        self.decision = DecisionMaker(config)
        self.motion = MotionPlanner(config)
        self.safety = SafetyChecker(config)
        self.predictor = TrajectoryPredictor(config)
        self.graph_builder = SceneGraphBuilder()

    def plan(self, perception: Optional[PerceptionResult] = None,
             image: Optional[object] = None) -> dict:
        """生成驾驶指令 + 自车轨迹 + 安全校验结果。"""
        scene = perception.scene_graph if perception else None
        model_cmd = self._model_command(scene, image)
        command = self.decision.decide(scene, model_cmd)
        traj = self._trajectory_for(command)
        others = (perception.detections if perception else []) or []
        safe = self.safety.is_safe(traj, others)
        return {
            "command": command,
            "trajectory": traj,
            "safe": safe,
            "model_raw": model_cmd,
            "scene_summary": self.graph_builder.summarize(scene) if scene else "",
        }

    def _model_command(self, scene: Optional[SceneGraph], image: Optional[object]) -> str:
        summary = self.graph_builder.summarize(scene) if scene else "未知场景"
        prompt = planning_prompt(summary, self.config.target_speed)
        if image is not None:
            raw = self.engine.generate(prompt, image=image, system=SYSTEM_PLANNING)
            return classify_action(raw)
        return "KEEP_LANE"

    def _trajectory_for(self, command: DrivingCommand) -> Trajectory:
        action = command.action
        if action == "STOP":
            return self.motion.stop()
        if action == "SLOW_DOWN":
            return self.motion.straight(self.config.target_speed * 0.4)
        if action == "CHANGE_LANE":
            return self.motion.lane_change()
        if action in ("TURN_LEFT", "TURN_RIGHT"):
            return self.motion.lane_change(target_lane_offset=2.0)
        return self.motion.straight()

    def predict_trajectories(self, detections: List) -> List[Trajectory]:
        return self.predictor.predict_all(detections)
