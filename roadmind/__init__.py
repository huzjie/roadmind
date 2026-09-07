"""RoadMind — 自动驾驶视觉语言模型推理与规划平台。

围绕首个面向自动驾驶的视觉语言基础模型（Qwen-Drive）构建的工程化平台：
统一 3D 感知、场景视觉问答、轨迹预测与运动规划，并提供多后端推理、
OpenAI 兼容 REST API、CLI 与 Python SDK。

本包为顶层入口，导出核心版本信息与常用符号。
"""
from roadmind.version import __version__, __author__, __license__

__all__ = ["__version__", "__author__", "__license__"]
