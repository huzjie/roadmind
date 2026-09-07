"""驾驶场景数据集抽象。"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator, List, Optional


class DrivingDataset:
    """从目录加载图像帧的简单数据集，可迭代出 (image, meta)。"""

    SUPPORTED = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

    def __init__(self, root: str, extensions: Optional[tuple] = None) -> None:
        self.root = Path(root)
        self.extensions = extensions or self.SUPPORTED
        self._files = self._scan()

    def _scan(self) -> List[Path]:
        if not self.root.exists():
            return []
        out = []
        for p in self.root.rglob("*"):
            if p.suffix.lower() in self.extensions:
                out.append(p)
        return sorted(out)

    def __len__(self) -> int:
        return len(self._files)

    def __getitem__(self, idx: int) -> Any:
        path = self._files[idx]
        return self._load(path)

    def _load(self, path: Path) -> Any:
        try:
            from PIL import Image
            return Image.open(path).convert("RGB")
        except ImportError:
            return str(path)

    def __iter__(self) -> Iterator[Any]:
        for i in range(len(self)):
            yield self[i]
