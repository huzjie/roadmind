"""轻量文本工具：计数、截断、拼接（不依赖真实 tokenizer）。"""
from __future__ import annotations

from typing import List


def approximate_tokens(text: str) -> int:
    """粗略估算 token 数：英文按空格，中文按字符。"""
    if not text:
        return 0
    words = text.split()
    cjk = sum(1 for ch in text if "一" <= ch <= "鿿")
    non_cjk_chars = sum(1 for ch in text if not ch.isspace()) - cjk
    return max(len(words), 1) + cjk + (non_cjk_chars // 4)


def truncate_text(text: str, max_tokens: int) -> str:
    """按 token 预算截断文本。"""
    if approximate_tokens(text) <= max_tokens:
        return text
    out: List[str] = []
    used = 0
    for word in text.split():
        cost = approximate_tokens(word) + 1
        if used + cost > max_tokens:
            break
        out.append(word)
        used += cost
    return " ".join(out)
