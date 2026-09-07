"""交通要素（灯 / 标志）抽取。"""
from __future__ import annotations

from typing import Any, List, Optional

from roadmind.core.types import TrafficLight, TrafficSign
from roadmind.inference.engine import InferenceEngine


class TrafficElementExtractor:
    """从图像抽取交通灯与标志。"""

    def __init__(self, engine: InferenceEngine) -> None:
        self.engine = engine

    def extract(self, image: Optional[Any] = None) -> tuple:
        if image is None:
            return [], []
        raw = self.engine.generate("列出交通灯颜色与交通标志。", image=image)
        return self._parse(raw)

    def _parse(self, raw: str) -> tuple:
        lights: List[TrafficLight] = []
        signs: List[TrafficSign] = []
        text = (raw or "").lower()
        for i, state in enumerate(("red", "green", "yellow")):
            if state in text:
                lights.append(TrafficLight(light_id=i, state=state))
        for i, st in enumerate(("stop", "yield", "speed_limit", "no_entry", "crosswalk")):
            if st in text:
                signs.append(TrafficSign(sign_id=i, sign_type=st))
        return lights, signs
