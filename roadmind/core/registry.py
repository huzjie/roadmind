"""模型与后端的注册表，支持动态注册与查找。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from roadmind.core.exceptions import BackendNotFoundError
from roadmind.core.types import ModelCard


@dataclass
class BackendRegistry:
    """推理后端注册表：名称 -> 工厂函数。"""

    _factories: Dict[str, Callable[..., Any]] = field(default_factory=dict)

    def register(self, name: str, factory: Callable[..., Any]) -> None:
        self._factories[name] = factory

    def names(self) -> List[str]:
        return sorted(self._factories.keys())

    def has(self, name: str) -> bool:
        return name in self._factories

    def create(self, name: str, **kwargs: Any) -> Any:
        if name not in self._factories:
            raise BackendNotFoundError(
                "未知推理后端 " + repr(name) + "，可用：" + ", ".join(self.names())
            )
        return self._factories[name](**kwargs)


@dataclass
class ModelRegistry:
    """模型目录：按名称维护 ModelCard。"""

    _cards: Dict[str, ModelCard] = field(default_factory=dict)

    def add(self, card: ModelCard) -> None:
        self._cards[card.name] = card

    def get(self, name: str) -> Optional[ModelCard]:
        return self._cards.get(name)

    def list(self, task: Optional[str] = None, backend: Optional[str] = None) -> List[ModelCard]:
        out = list(self._cards.values())
        if task:
            out = [c for c in out if c.task == task]
        if backend:
            out = [c for c in out if c.backend == backend]
        return out

    def __len__(self) -> int:
        return len(self._cards)
