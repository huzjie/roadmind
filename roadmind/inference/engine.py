"""统一推理引擎：按配置选后端、支持回退与缓存。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from roadmind.config.schema import InferenceConfig
from roadmind.core.exceptions import InferenceError
from roadmind.core.logging import get_logger
from roadmind.core.registry import BackendRegistry
from roadmind.inference.backends.base import BaseBackend
from roadmind.inference.cache import ResponseCache

logger = get_logger("roadmind.inference")


class InferenceEngine:
    """对上层暴露统一的 generate / describe 接口。"""

    def __init__(self, config: InferenceConfig, registry: BackendRegistry,
                 cache: Optional[ResponseCache] = None) -> None:
        self.config = config
        self.registry = registry
        self.cache = cache or (ResponseCache(ttl=config.cache_ttl) if config.cache_enabled else None)
        self._backend: Optional[BaseBackend] = None
        self._backend_name: Optional[str] = None

    def _build(self, name: str) -> BaseBackend:
        kwargs: Dict[str, Any] = {
            "model": self.config.model.name,
            "device": self.config.model.device,
            "dtype": self.config.model.dtype,
            "max_new_tokens": self.config.model.max_new_tokens,
            "temperature": self.config.model.temperature,
        }
        return self.registry.create(name, **kwargs)

    def _load_backend(self, name: str) -> BaseBackend:
        try:
            return self._build(name)
        except Exception as exc:  # noqa: BLE001
            logger.warning("后端 %s 加载失败：%s", name, exc)
            raise

    def backend(self) -> BaseBackend:
        """惰性加载主后端，失败则按 fallback 顺序降级。"""
        if self._backend is not None:
            return self._backend
        candidates = [self.config.model.backend] + list(self.config.fallback_backends)
        last_err: Optional[Exception] = None
        for name in candidates:
            try:
                self._backend = self._load_backend(name)
                self._backend_name = name
                logger.info("推理后端就绪：%s", name)
                return self._backend
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                logger.warning("后端 %s 不可用，尝试下一个", name)
        raise InferenceError("所有推理后端均不可用：" + str(last_err))

    def generate(self, prompt: str, image: Optional[Any] = None,
                 system: Optional[str] = None, **kwargs: Any) -> str:
        """生成文本；image 为可选图像输入（PIL/np.ndarray/路径）。"""
        if self.cache is not None:
            key = self.cache.key(prompt, image, system)
            hit = self.cache.get(key)
            if hit is not None:
                return hit
        out = self.backend().generate(prompt, image=image, system=system, **kwargs)
        if self.cache is not None:
            self.cache.put(key if "key" in locals() else self.cache.key(prompt, image, system), out)
        return out

    def describe(self) -> Dict[str, Any]:
        """描述当前后端与模型信息。"""
        backend = self.backend()
        return {
            "backend": self._backend_name,
            "model": self.config.model.name,
            "info": backend.info(),
        }
