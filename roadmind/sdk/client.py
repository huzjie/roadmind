"""RoadMind 远程客户端（纯 stdlib）。"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib import request, error as urlerror


class RoadMindClient:
    """访问 RoadMind HTTP 服务的客户端。"""

    def __init__(self, base_url: str = "http://127.0.0.1:8000/v1",
                 timeout: int = 120) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(self.base_url + path, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urlerror.URLError as exc:
            raise ConnectionError("RoadMind 服务调用失败：" + str(exc)) from exc

    def _get(self, path: str) -> Dict[str, Any]:
        req = request.Request(self.base_url + path)
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urlerror.URLError as exc:
            raise ConnectionError("RoadMind 服务调用失败：" + str(exc)) from exc

    def health(self) -> Dict[str, Any]:
        return self._get("/health")

    def generate(self, prompt: str, image: Optional[str] = None,
                 system: Optional[str] = None) -> Dict[str, Any]:
        return self._post("/generate", {"prompt": prompt, "image": image, "system": system})

    def perceive(self, image: Optional[str] = None) -> Dict[str, Any]:
        return self._post("/perceive", {"image": image})

    def plan(self) -> Dict[str, Any]:
        return self._post("/plan", {})

    def models(self) -> Dict[str, Any]:
        return self._get("/models")
