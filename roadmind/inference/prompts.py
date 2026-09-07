"""提示词模板库（感知 / 问答 / 规划）。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


SYSTEM_VISION = (
    "你是自动驾驶视觉语言助手，能够理解前视摄像头画面并给出驾驶相关判断。"
    "回答务必简洁、可执行、安全优先。"
)

SYSTEM_PLANNING = (
    "你是自动驾驶运动规划器，根据场景描述输出高层驾驶指令。"
    "只能从 STOP / SLOW_DOWN / KEEP_LANE / TURN_LEFT / TURN_RIGHT / CHANGE_LANE 中选择。"
)


def perception_prompt(instruction: str = "描述画面中的目标、车道线和交通信号。") -> str:
    """构建感知提示词。"""
    return "请观察图像，" + instruction


def vqa_prompt(question: str) -> str:
    """构建视觉问答提示词。"""
    return "请根据图像回答：" + question


def planning_prompt(scene_summary: str, target_speed: float) -> str:
    """构建规划提示词。"""
    return (
        "场景：{0}。目标车速 {1} m/s。"
        "请输出一个高层驾驶指令（STOP / SLOW_DOWN / KEEP_LANE / TURN_LEFT / TURN_RIGHT / CHANGE_LANE）。"
    ).format(scene_summary, target_speed)


def classify_action(text: str) -> str:
    """从模型原始输出里提取规范指令。"""
    upper = (text or "").upper()
    for action in ("STOP", "SLOW_DOWN", "KEEP_LANE", "TURN_LEFT", "TURN_RIGHT", "CHANGE_LANE"):
        if action in upper:
            return action
    return "KEEP_LANE"
