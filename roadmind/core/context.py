"""运行时上下文：承载配置、模型目录与全局状态。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from roadmind.config.schema import AppConfig
from roadmind.core.registry import BackendRegistry, ModelRegistry


@dataclass
class RuntimeContext:
    """贯穿一次运行的共享上下文。"""

    config: AppConfig
    models: ModelRegistry = field(default_factory=ModelRegistry)
    backends: BackendRegistry = field(default_factory=BackendRegistry)
    cache: Dict[str, Any] = field(default_factory=dict)
    extras: Dict[str, Any] = field(default_factory=dict)

    @property
    def app_name(self) -> str:
        return self.config.app.name

    def set(self, key: str, value: Any) -> None:
        self.extras[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.extras.get(key, default)
