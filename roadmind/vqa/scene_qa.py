"""场景视觉问答。"""
from __future__ import annotations

from typing import Any, Optional

from roadmind.core.types import VQAResult
from roadmind.inference.engine import InferenceEngine
from roadmind.inference.prompts import SYSTEM_VISION, vqa_prompt


class SceneQA:
    """通用场景问答。"""

    def __init__(self, engine: InferenceEngine) -> None:
        self.engine = engine

    def ask(self, question: str, image: Optional[Any] = None) -> VQAResult:
        raw = self.engine.generate(vqa_prompt(question), image=image, system=SYSTEM_VISION)
        return VQAResult(question=question, answer=raw, raw=raw)
