"""评测执行器。"""
from __future__ import annotations

from typing import Callable, Dict, List

from roadmind.core.exceptions import EvaluationError
from roadmind.core.logging import get_logger

logger = get_logger("roadmind.eval")


class Evaluator:
    """运行一组评测用例，汇总指标。"""

    def __init__(self) -> None:
        self._cases: List[tuple] = []

    def add(self, name: str, fn: Callable[[], dict]) -> None:
        self._cases.append((name, fn))

    def run(self) -> Dict[str, dict]:
        results: Dict[str, dict] = {}
        for name, fn in self._cases:
            try:
                results[name] = fn()
            except Exception as exc:  # noqa: BLE001
                logger.warning("评测 %s 失败：%s", name, exc)
                results[name] = {"error": str(exc)}
        return results
