"""统一目标检测器：对接推理引擎做 2D/3D 检测。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from roadmind.config.schema import PerceptionConfig
from roadmind.core.logging import get_logger
from roadmind.core.types import BoundingBox2D, BoundingBox3D, Detection
from roadmind.inference.engine import InferenceEngine
from roadmind.inference.prompts import SYSTEM_VISION, perception_prompt

logger = get_logger("roadmind.perception")


class Detector:
    """基于视觉语言模型的检测器，同时支持规则化后处理。"""

    def __init__(self, config: PerceptionConfig, engine: InferenceEngine) -> None:
        self.config = config
        self.engine = engine

    def detect(self, image: Optional[Any] = None, prompt: Optional[str] = None) -> List[Detection]:
        """返回检测列表。无图像时返回空列表。"""
        if image is None:
            return []
        raw = self.engine.generate(
            perception_prompt(prompt or "列出所有交通参与者及其位置。"),
            image=image,
            system=SYSTEM_VISION,
        )
        return self._parse(raw)

    def _parse(self, raw: str) -> List[Detection]:
        """把模型文本输出解析为结构化检测（容错）。"""
        dets: List[Detection] = []
        text = (raw or "").lower()
        # 常见类别粗匹配
        for label in ("car", "pedestrian", "person", "cyclist", "truck", "bus", "motorcycle", "traffic_light", "traffic_sign"):
            if label.replace("_", " ") in text or label in text:
                dets.append(Detection(label=label.replace("_", " "), confidence=0.9))
        # 去重保序
        seen = set()
        out: List[Detection] = []
        for d in dets:
            if d.label not in seen:
                seen.add(d.label)
                out.append(d)
        return out


class BEVExtractor:
    """BEV（鸟瞰图）特征占位实现：真实实现挂载视觉主干。"""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def extract(self, image: Optional[Any] = None) -> Optional[Any]:
        if not self.enabled or image is None:
            return None
        # 占位：真实部署时返回视觉主干的 BEV 特征张量
        return {"shape": None, "dummy": True}
