"""图像 / 张量变换。"""
from __future__ import annotations

from typing import Any, Callable, List


class Resize:
    """调整图像尺寸（PIL）。"""

    def __init__(self, size: tuple) -> None:
        self.size = size

    def __call__(self, image: Any) -> Any:
        if hasattr(image, "resize"):
            return image.resize(self.size)
        return image


class ToTensor:
    """PIL -> 张量（需 torch；无 torch 则透传）。"""

    def __call__(self, image: Any) -> Any:
        try:
            from torchvision import transforms
            return transforms.ToTensor()(image)
        except ImportError:
            return image


class Compose:
    """顺序组合多个变换。"""

    def __init__(self, transforms: List[Callable]) -> None:
        self.transforms = transforms

    def __call__(self, x: Any) -> Any:
        for t in self.transforms:
            x = t(x)
        return x
