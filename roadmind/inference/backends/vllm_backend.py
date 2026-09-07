"""vLLM 高吞吐后端（懒加载）。"""
from __future__ import annotations

from typing import Any, Dict, Optional

from roadmind.core.exceptions import ModelLoadError
from roadmind.core.logging import get_logger
from roadmind.inference.backends.base import BaseBackend

logger = get_logger("roadmind.inference.vllm")


class VLLMBackend(BaseBackend):
    """基于 vLLM 的批量 / 高吞吐推理后端。"""

    name = "vllm"

    def __init__(self, model: str, device: str = "auto", dtype: str = "auto",
                 max_new_tokens: int = 512, temperature: float = 0.2,
                 tensor_parallel: int = 1, **kwargs: Any) -> None:
        super().__init__(model, device, dtype, max_new_tokens, temperature)
        self.tensor_parallel = tensor_parallel
        self._llm = None

    def _load(self) -> None:
        if self._llm is not None:
            return
        try:
            from vllm import LLM, SamplingParams
        except ImportError as exc:
            raise ModelLoadError("缺少 vllm，请 pip install roadmind[vllm]") from exc
        try:
            self._llm = LLM(model=self.model, tensor_parallel_size=self.tensor_parallel,
                            dtype=self.dtype if self.dtype != "auto" else "auto")
            self._sampling = SamplingParams(temperature=self.temperature,
                                            max_tokens=self.max_new_tokens)
            logger.info("vLLM 后端加载完成：%s", self.model)
        except Exception as exc:  # noqa: BLE001
            raise ModelLoadError("vLLM 加载模型失败：" + str(exc)) from exc

    def generate(self, prompt: str, image: Optional[Any] = None,
                 system: Optional[str] = None, **kwargs: Any) -> str:
        self._load()
        text = prompt if system is None else system + chr(10) + prompt
        out = self._llm.generate([text], self._sampling)
        return out[0].outputs[0].text if out and out[0].outputs else ""

    def info(self) -> Dict[str, Any]:
        return {"backend": self.name, "model": self.model, "loaded": self._llm is not None}
