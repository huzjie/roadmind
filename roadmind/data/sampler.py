"""采样器：均衡 / 随机。"""
from __future__ import annotations

import random
from typing import List


def balanced_sample(items: List, k: int, seed: int = 0) -> List:
    """确定性随机采样。"""
    rng = random.Random(seed)
    if k >= len(items):
        return list(items)
    return rng.sample(items, k)


def round_robin(groups: List[List], k: int) -> List:
    """从多个分组轮流取样。"""
    out: List = []
    idx = 0
    while len(out) < k:
        group = groups[idx % len(groups)]
        if group:
            out.append(group[(idx // len(groups)) % len(group)])
        idx += 1
        if all(len(g) == 0 for g in groups):
            break
    return out
