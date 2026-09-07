"""HuggingFace Transformers 后端（懒加载，需 torch + transformers）。"""
from __future__ import annotations

from typing import Any, Dict, Optional

from roadmind.core.exceptions import ModelLoadError
from roadmind.core.logging import get_logger
from roadmind.inference.backends.base import BaseBackend

logger = get_logger("roadmind.inference.transformers")


class TransformersBackend(BaseBackend):
    """基于 AutoModelForCausalLM / VLM pipeline 的本地推理后端。"""

    name = "transformers"

    def __init__(self, model: str, device: str = "auto", dtype: str = "auto",
                 max_new_tokens: int = 512, temperature: float = 0.2,
                 trust_remote_code: bool = False, **kwargs: Any) -> None:
        super().__init__(model, device, dtype, max_new_tokens, temperature)
        self.trust_remote_code = trust_remote_code
        self._pipe = None

    def _load(self) -> None:
        if self._pipe is not None:
            return
        try:
            import torch  # noqa: F401
            from transformers import pipeline
        except ImportError as exc:
            raise ModelLoadError("缺少 torch/transformers，请 pip install roadmind[torch]") from exc
        try:
            self._pipe = pipeline(
                "image-text-to-text",
                model=self.model,
                device=self.device,
                torch_dtype=self.dtype if self.dtype != "auto" else "auto",
                trust_remote_code=self.trust_remote_code,
                max_new_tokens=self.max_new_tokens,
            )
            logger.info("transformers 后端加载完成：%s", self.model)
        except Exception as exc:  # noqa: BLE001
            raise ModelLoadError("transformers 加载模型失败：" + str(exc)) from exc

    def generate(self, prompt: str, image: Optional[Any] = None,
                 system: Optional[str] = None, **kwargs: Any) -> str:
        self._load()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        content: Any = prompt
        if image is not None:
            content = [{"type": "image"}, {"type": "text", "text": prompt}]
        messages.append({"role": "user", "content": content})
        out = self._pipe(messages, temperature=self.temperature)
        return str(out[0]["generated_text"]) if out else ""

    def info(self) -> Dict[str, Any]:
        return {"backend": self.name, "model": self.model, "loaded": self._pipe is not None}
