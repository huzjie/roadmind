"""配置数据模型（dataclass，无重依赖）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AppSection:
    name: str = "roadmind"
    version: str = "1.0.0"
    timezone: str = "Asia/Shanghai"
    log_level: str = "INFO"


@dataclass
class ModelConfig:
    name: str = "Qwen/Qwen-Drive-1.0-4B"
    backend: str = "transformers"
    device: str = "auto"
    dtype: str = "auto"
    max_new_tokens: int = 512
    temperature: float = 0.2
    trust_remote_code: bool = False
    revision: str = "main"
    cache_dir: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InferenceConfig:
    model: ModelConfig = field(default_factory=ModelConfig)
    fallback_backends: List[str] = field(default_factory=lambda: ["mock"])
    cache_enabled: bool = True
    cache_ttl: int = 300
    timeout: int = 120
    batch_size: int = 1


@dataclass
class PerceptionConfig:
    backend: str = "roadmind"
    conf_threshold: float = 0.3
    nms_iou: float = 0.45
    enable_bev: bool = True
    enable_tracking: bool = True
    max_detections: int = 100


@dataclass
class PlanningConfig:
    horizon: float = 6.0
    dt: float = 0.5
    max_speed: float = 15.0
    target_speed: float = 10.0
    safety_margin: float = 2.0
    lane_width: float = 3.5


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    api_prefix: str = "/v1"
    enable_docs: bool = True


@dataclass
class ObservabilityConfig:
    metrics_enabled: bool = True
    tracing_enabled: bool = False
    prometheus_enabled: bool = False
    log_payload: bool = False


@dataclass
class AppConfig:
    app: AppSection = field(default_factory=AppSection)
    inference: InferenceConfig = field(default_factory=InferenceConfig)
    perception: PerceptionConfig = field(default_factory=PerceptionConfig)
    planning: PlanningConfig = field(default_factory=PlanningConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)

    def to_dict(self) -> Dict[str, Any]:
        from dataclasses import asdict
        return asdict(self)
