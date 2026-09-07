"""OpenAI 兼容 API 后端（远程）。"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional
from urllib import request, error as urlerror

from roadmind.core.exceptions import InferenceError
from roadmind.inference.backends.base import BaseBackend


class OpenAICompatibleBackend(BaseBackend):
    """对接任意 OpenAI 兼容 /v1/chat/completions 端点。"""

    name = "openai"

    def __init__(self, model: str, device: str = "auto", dtype: str = "auto",
                 max_new_tokens: int = 512, temperature: float = 0.2,
                 base_url: Optional[str] = None, api_key: Optional[str] = None,
                 **kwargs: Any) -> None:
        super().__init__(model, device, dtype, max_new_tokens, temperature)
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")

    def generate(self, prompt: str, image: Optional[Any] = None,
                 system: Optional[str] = None, **kwargs: Any) -> str:
        messages: list = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_new_tokens,
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(self.base_url + "/chat/completions", data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", "Bearer " + self.api_key)
        try:
            with request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return str(body["choices"][0]["message"]["content"])
        except (urlerror.URLError, TimeoutError, KeyError, IndexError) as exc:
            raise InferenceError("OpenAI 兼容端点调用失败：" + str(exc)) from exc

    def info(self) -> Dict[str, Any]:
        return {"backend": self.name, "model": self.model, "base_url": self.base_url}
