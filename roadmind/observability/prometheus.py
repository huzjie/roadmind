"""Prometheus 指标导出（懒加载 prometheus_client）。"""
from __future__ import annotations

from typing import Any, Optional

from roadmind.observability.metrics import Metrics


def render_prometheus(metrics: Metrics) -> str:
    """把 Metrics 快照渲染为 Prometheus 文本格式。"""
    snap = metrics.snapshot()
    lines: list = []
    for name, value in snap["counters"].items():
        safe = name.replace(".", "_").replace("-", "_")
        lines.append(f"# TYPE {safe} counter")
        lines.append(f"{safe} {value}")
    for name, item in snap["latency"].items():
        safe = name.replace(".", "_").replace("-", "_")
        lines.append(f"# TYPE {safe}_seconds gauge")
        lines.append(f"{safe}_seconds {item['avg_s']:.6f}")
    lines.append("")
    return chr(10).join(lines)
