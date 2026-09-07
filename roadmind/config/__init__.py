"""配置子系统：加载、校验 YAML 配置。"""
from roadmind.config.loader import load_config, load_config_from_dict
from roadmind.config.schema import (
    AppConfig,
    AppSection,
    InferenceConfig,
    ModelConfig,
    ObservabilityConfig,
    PerceptionConfig,
    PlanningConfig,
    ServerConfig,
)

__all__ = [
    "AppConfig",
    "AppSection",
    "InferenceConfig",
    "ModelConfig",
    "ObservabilityConfig",
    "PerceptionConfig",
    "PlanningConfig",
    "ServerConfig",
    "load_config",
    "load_config_from_dict",
]
