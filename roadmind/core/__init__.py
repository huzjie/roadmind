"""核心基础模块：类型、异常、注册表、日志、运行时上下文。"""
from roadmind.core.exceptions import (
    RoadMindError,
    ConfigError,
    BackendNotFoundError,
    ModelLoadError,
    InferenceError,
    PerceptionError,
    PlanningError,
    EvaluationError,
)
from roadmind.core.registry import BackendRegistry, ModelRegistry

__all__ = [
    "RoadMindError",
    "ConfigError",
    "BackendNotFoundError",
    "ModelLoadError",
    "InferenceError",
    "PerceptionError",
    "PlanningError",
    "EvaluationError",
    "BackendRegistry",
    "ModelRegistry",
]
