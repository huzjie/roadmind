"""高层编排：感知 → 问答 → 规划 的端到端驾驶决策流水线。"""
from __future__ import annotations

from typing import Any, Optional

from roadmind.config.schema import AppConfig
from roadmind.core.context import RuntimeContext
from roadmind.core.logging import get_logger
from roadmind.inference.engine import InferenceEngine
from roadmind.perception.pipeline import PerceptionPipeline
from roadmind.planning.planner import Planner
from roadmind.vqa.risk_qa import RiskQA

logger = get_logger("roadmind.pipeline")


class DrivingPipeline:
    """一站式驾驶决策流水线，串联各子系统。"""

    def __init__(self, config: AppConfig, engine: InferenceEngine) -> None:
        self.config = config
        self.engine = engine
        self.perception = PerceptionPipeline(config.perception, engine)
        self.planner = Planner(config.planning, engine)
        self.risk = RiskQA(engine)

    def run(self, image: Optional[Any] = None) -> dict:
        """输入一帧图像，输出感知 + 风险 + 规划结果。"""
        perception = self.perception.run(image)
        plan = self.planner.plan(perception, image)
        risk = self.risk.assess(image) if image is not None else None
        return {
            "perception": perception,
            "plan": plan,
            "risk": risk,
        }

    def summarize(self, result: dict) -> str:
        """把流水线结果压缩成一行可读摘要。"""
        plan = result["plan"]
        cmd = plan["command"]
        perception = result["perception"]
        dets = ", ".join(sorted({d.label for d in perception.detections})) or "无目标"
        risk_txt = result["risk"].answer if result.get("risk") else "未评估"
        return (
            "指令={0}({1}) | 目标={2} | 安全={3} | 风险={4}"
        ).format(cmd.action, cmd.reason, dets, plan["safe"], risk_txt)
