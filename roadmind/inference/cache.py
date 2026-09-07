"""简单内存响应缓存（TTL + 哈希键）。"""
from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, Optional, Tuple


class ResponseCache:
    """线程不安全的轻量 TTL 缓存，用于避免重复推理。"""

    def __init__(self, ttl: int = 300, max_size: int = 1024) -> None:
        self.ttl = ttl
        self.max_size = max_size
        self._store: Dict[str, Tuple[float, str]] = {}

    def key(self, prompt: str, image: Optional[Any] = None, system: Optional[str] = None) -> str:
        raw = (system or "") + "|" + prompt
        if image is not None:
            raw += "|image:" + str(id(image)) if not isinstance(image, str) else "|image:" + image
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, key: str) -> Optional[str]:
        item = self._store.get(key)
        if item is None:
            return None
        ts, value = item
        if time.time() - ts > self.ttl:
            self._store.pop(key, None)
            return None
        return value

    def put(self, key: str, value: str) -> None:
        if len(self._store) >= self.max_size:
            oldest = min(self._store, key=lambda k: self._store[k][0])
            self._store.pop(oldest, None)
        self._store[key] = (time.time(), value)

    def clear(self) -> None:
        self._store.clear()

    def __len__(self) -> int:
        return len(self._store)
