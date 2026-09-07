"""统一日志配置。"""
from __future__ import annotations

import logging
import sys
from typing import Optional

_FMT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
_DEFAULT_LEVEL = logging.INFO


def setup_logging(level: Optional[str] = None, verbose: bool = False) -> None:
    """初始化根日志器，输出到 stderr。"""
    lvl = _DEFAULT_LEVEL
    if verbose:
        lvl = logging.DEBUG
    if level:
        lvl = getattr(logging, level.upper(), _DEFAULT_LEVEL)
    root = logging.getLogger()
    root.setLevel(lvl)
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_FMT))
        root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """获取命名日志器。"""
    return logging.getLogger(name)
