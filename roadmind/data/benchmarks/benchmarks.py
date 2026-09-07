"""内置评测基准元数据。"""
from __future__ import annotations

BENCHMARKS = {
    "nuplan_like": {
        "name": "nuplan-like",
        "tasks": ["trajectory_prediction", "motion_planning", "decision"],
        "metrics": ["ade", "fde", "collision_rate", "comfort_score"],
        "description": "类 nuPlan 的规划评测基准（本地模拟）。",
    },
    "drive_lm": {
        "name": "drive-lm",
        "tasks": ["vqa", "scene_understanding", "perception"],
        "metrics": ["accuracy", "rouge", "cider"],
        "description": "自动驾驶视觉语言理解评测基准。",
    },
    "perception_3d": {
        "name": "perception-3d",
        "tasks": ["3d_detection", "bev_segmentation", "lane_detection"],
        "metrics": ["map", "nds", "iou"],
        "description": "3D 感知评测基准。",
    },
}


def list_benchmarks() -> list:
    return list(BENCHMARKS.values())
