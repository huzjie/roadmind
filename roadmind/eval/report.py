"""评测报告渲染。"""
from __future__ import annotations

from typing import Dict


def render_report(results: Dict[str, dict]) -> str:
    """渲染为 Markdown 表格。"""
    lines = ["# 评测报告", ""]
    lines.append("| 用例 | 指标 | 值 |")
    lines.append("|---|---|---|")
    for name, metrics in results.items():
        if "error" in metrics:
            lines.append(f"| {name} | error | {metrics['error']} |")
            continue
        for key, value in metrics.items():
            lines.append(f"| {name} | {key} | {value} |")
    return chr(10).join(lines)
