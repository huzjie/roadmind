"""Ollama 本地后端（HTTP）。"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib import request, error as urlerror

from roadmind.core.exceptions import InferenceError
from roadmind.inference.backends.base import BaseBackend


class OllamaBackend(BaseBackend):
    """通过 Ollama 本地服务推理。"""

    name = "ollama"

    def __init__(self, model: str, device: str = "auto", dtype: str = "auto",
                 max_new_tokens: int = 512, temperature: float = 0.2,
                 base_url: str = "http://127.0.0.1:11434", **kwargs: Any) -> None:
        super().__init__(model, device, dtype, max_new_tokens, temperature)
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, image: Optional[Any] = None,
                 system: Optional[str] = None, **kwargs: Any) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.temperature, "num_predict": self.max_new_tokens},
        }
        if system:
            payload["system"] = system
        if image is not None:
            payload["images"] = [image] if isinstance(image, str) else None
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(self.base_url + "/api/generate", data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            with request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return str(body.get("response", ""))
        except (urlerror.URLError, TimeoutError) as exc:
            raise InferenceError("Ollama 调用失败：" + str(exc)) from exc

    def info(self) -> Dict[str, Any]:
        return {"backend": self.name, "model": self.model, "base_url": self.base_url}
