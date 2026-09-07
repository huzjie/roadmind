"""驾驶风险问答。"""
from __future__ import annotations

from typing import Any, Optional

from roadmind.core.types import VQAResult
from roadmind.inference.engine import InferenceEngine
from roadmind.inference.prompts import SYSTEM_VISION


class RiskQA:
    """识别潜在风险并给出建议。"""

    def __init__(self, engine: InferenceEngine) -> None:
        self.engine = engine

    def assess(self, image: Optional[Any] = None) -> VQAResult:
        q = "画面中是否存在碰撞风险？若存在，指出风险来源。"
        raw = self.engine.generate(q, image=image, system=SYSTEM_VISION)
        return VQAResult(question=q, answer=raw, raw=raw)
