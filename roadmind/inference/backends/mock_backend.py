"""离线 Mock 后端：无需模型即可跑通全链路，用于自检 / CI / 演示。"""
from __future__ import annotations

from typing import Any, Dict, Optional

from roadmind.inference.backends.base import BaseBackend


class MockBackend(BaseBackend):
    """返回确定性的伪输出，按 prompt 关键词分流。"""

    name = "mock"

    _KEYWORDS = {
        "stop": "STOP",
        "红灯": "STOP",
        "red light": "STOP",
        "行人": "SLOW_DOWN",
        "pedestrian": "SLOW_DOWN",
        "turn": "TURN",
        "left": "LEFT",
        "right": "RIGHT",
    }

    def generate(self, prompt: str, image: Optional[Any] = None,
                 system: Optional[str] = None, **kwargs: Any) -> str:
        lowered = (prompt or "").lower()
        for key, action in self._KEYWORDS.items():
            if key in lowered:
                return action + " | mock-backend deterministic output"
        if "规划" in prompt or "plan" in lowered:
            return "KEEP_LANE | mock-backend deterministic output"
        if "检测" in prompt or "detect" in lowered:
            return "detected: car, pedestrian | mock-backend deterministic output"
        return "OK | mock-backend deterministic output"

    def info(self) -> Dict[str, Any]:
        return {"backend": self.name, "model": self.model, "loaded": True, "offline": True}
