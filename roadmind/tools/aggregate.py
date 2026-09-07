"""结果聚合工具。"""
from __future__ import annotations

from typing import Dict, List


def aggregate_results(results: List[Dict]) -> Dict:
    """聚合多份规划结果，统计安全率与指令分布。"""
    total = len(results)
    if total == 0:
        return {"total": 0, "safe_rate": 0.0, "commands": {}}
    safe = sum(1 for r in results if r.get("safe"))
    commands: Dict[str, int] = {}
    for r in results:
        action = r.get("command", {}).get("action", "UNKNOWN") if isinstance(r.get("command"), dict) else "UNKNOWN"
        commands[action] = commands.get(action, 0) + 1
    return {"total": total, "safe_rate": safe / total, "commands": commands}
