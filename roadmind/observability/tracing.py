"""轻量追踪（跨度树）。"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional


class Span:
    """单次操作跨度。"""

    def __init__(self, name: str, parent: Optional["Span"] = None) -> None:
        self.name = name
        self.parent = parent
        self.children: List["Span"] = []
        self.start = time.perf_counter()
        self.end: Optional[float] = None
        self.attrs: Dict[str, Any] = {}

    def set_attr(self, key: str, value: Any) -> None:
        self.attrs[key] = value

    def finish(self) -> None:
        self.end = time.perf_counter()

    @property
    def duration(self) -> float:
        end = self.end if self.end is not None else time.perf_counter()
        return end - self.start


class Tracer:
    """极简 span 追踪器。"""

    def __init__(self) -> None:
        self._root: List[Span] = []

    def start(self, name: str) -> Span:
        span = Span(name)
        self._root.append(span)
        return span

    def dump(self) -> List[Dict[str, Any]]:
        out = []
        for span in self._root:
            out.append({"name": span.name, "duration": span.duration, "attrs": span.attrs})
        return out
