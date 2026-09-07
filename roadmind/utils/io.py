"""IO 工具。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional


def read_text(path: str, encoding: str = "utf-8") -> str:
    """读取文本文件。"""
    return Path(path).read_text(encoding=encoding)


def write_json(obj: Any, path: str) -> None:
    """写 JSON 文件（自动建目录）。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def load_image(path: str) -> Any:
    """加载图像，返回 numpy 数组或 PIL 图像。"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError("图像不存在：" + path)
    try:
        from PIL import Image
        return Image.open(p).convert("RGB")
    except ImportError:
        raise ImportError("需要 Pillow：pip install roadmind[vision]")
