"""轻量指标计数器。"""
from __future__ import annotations

import threading
import time
from typing import Dict, List, Optional


class Metrics:
    """线程安全的内存计数器 + 延迟直方图。"""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: Dict[str, int] = {}
        self._latency: Dict[str, List[float]] = {}

    def incr(self, name: str, value: int = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + value

    def observe(self, name: str, seconds: float) -> None:
        with self._lock:
            self._latency.setdefault(name, []).append(seconds)

    def snapshot(self) -> Dict[str, object]:
        with self._lock:
            counters = dict(self._counters)
            latency = {
                k: {"count": len(v), "avg_s": (sum(v) / len(v)) if v else 0.0}
                for k, v in self._latency.items()
            }
        return {"counters": counters, "latency": latency}

    def reset(self) -> None:
        with self._lock:
            self._counters.clear()
            self._latency.clear()


class LatencyRecorder:
    """配合 Metrics 记录某操作耗时。"""

    def __init__(self, metrics: Metrics, name: str) -> None:
        self.metrics = metrics
        self.name = name
        self._start = time.perf_counter()

    def done(self) -> float:
        elapsed = time.perf_counter() - self._start
        self.metrics.observe(self.name, elapsed)
        self.metrics.incr(self.name + "_calls")
        return elapsed
