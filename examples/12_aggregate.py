"""结果聚合示例。"""
from roadmind.tools.aggregate import aggregate_results

results = [
    {"safe": True, "command": {"action": "KEEP_LANE"}},
    {"safe": True, "command": {"action": "KEEP_LANE"}},
    {"safe": False, "command": {"action": "STOP"}},
]
print(aggregate_results(results))
