"""感知流水线：把检测 / BEV / 车道线 / 信号灯串起来。"""
from __future__ import annotations

from typing import Any, Optional

from roadmind.config.schema import PerceptionConfig
from roadmind.core.logging import get_logger
from roadmind.core.types import PerceptionResult, SceneGraph
from roadmind.inference.engine import InferenceEngine
from roadmind.perception.detector import BEVExtractor, Detector
from roadmind.perception.lane import LaneDetector
from roadmind.scene.graph import SceneGraphBuilder

logger = get_logger("roadmind.perception")


class PerceptionPipeline:
    """高层感知入口：run(image) -> PerceptionResult。"""

    def __init__(self, config: PerceptionConfig, engine: InferenceEngine) -> None:
        self.config = config
        self.detector = Detector(config, engine)
        self.bev = BEVExtractor(config.enable_bev)
        self.lane_detector = LaneDetector(config.conf_threshold)
        self.graph_builder = SceneGraphBuilder()

    def run(self, image: Optional[Any] = None) -> PerceptionResult:
        detections = self.detector.detect(image)
        bev = self.bev.extract(image)
        lanes = self.lane_detector.detect(image)
        graph = self.graph_builder.build(detections, lanes) if detections or lanes else None
        return PerceptionResult(
            detections=detections,
            lanes=lanes,
            bev_features=bev,
            scene_graph=graph,
            metadata={"pipeline": "roadmind-v1"},
        )
