"""推理后端实现集合。"""
from roadmind.inference.backends.base import BaseBackend
from roadmind.inference.backends.mock_backend import MockBackend

__all__ = ["BaseBackend", "MockBackend"]
