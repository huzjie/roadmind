"""后端抽象基类。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseBackend(ABC):
    """所有推理后端实现 generate / info 的统一契约。"""

    name: str = "base"

    def __init__(self, model: str, device: str = "auto", dtype: str = "auto",
                 max_new_tokens: int = 512, temperature: float = 0.2) -> None:
        self.model = model
        self.device = device
        self.dtype = dtype
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

    @abstractmethod
    def generate(self, prompt: str, image: Optional[Any] = None,
                 system: Optional[str] = None, **kwargs: Any) -> str:
        """执行一次生成，返回文本。"""

    @abstractmethod
    def info(self) -> Dict[str, Any]:
        """返回后端元信息。"""
