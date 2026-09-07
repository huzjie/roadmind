"""交通要素问答。"""
from __future__ import annotations

from typing import Any, Optional

from roadmind.core.types import VQAResult
from roadmind.inference.engine import InferenceEngine
from roadmind.inference.prompts import SYSTEM_VISION


class TrafficQA:
    """面向交通信号 / 标志 / 道路规则的理解问答。"""

    def __init__(self, engine: InferenceEngine) -> None:
        self.engine = engine

    def light_state(self, image: Optional[Any] = None) -> VQAResult:
        return self._ask("前方交通灯当前是什么颜色？", image)

    def sign_type(self, image: Optional[Any] = None) -> VQAResult:
        return self._ask("画面中有哪些交通标志？", image)

    def _ask(self, question: str, image: Optional[Any]) -> VQAResult:
        raw = self.engine.generate(question, image=image, system=SYSTEM_VISION)
        return VQAResult(question=question, answer=raw, raw=raw)
