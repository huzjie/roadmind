"""感知模块测试。"""
from roadmind.config.loader import load_config
from roadmind.inference.engine import InferenceEngine


def test_perception_empty(mock_engine):
    from roadmind.perception.pipeline import PerceptionPipeline
    pipeline = PerceptionPipeline(load_config().perception, mock_engine)
    result = pipeline.run(None)
    assert result.detections == []


def test_fusion():
    from roadmind.perception.fusion import SensorFusion
    from roadmind.core.types import Detection, PerceptionResult
    a = PerceptionResult(detections=[Detection(label="car")])
    b = PerceptionResult(detections=[Detection(label="car"), Detection(label="pedestrian")])
    merged = SensorFusion().fuse([a, b])
    assert len(merged.detections) == 2
