"""注册自定义模型与后端示例。"""
from roadmind.config.loader import load_config
from roadmind.core.context import RuntimeContext
from roadmind.core.types import ModelCard
from roadmind.inference.backends.mock_backend import MockBackend
from roadmind.inference.engine import InferenceEngine

config = load_config()
ctx = RuntimeContext(config=config)
ctx.backends.register("mock", MockBackend)
ctx.models.add(ModelCard(name="my/qwen-drive", family="Qwen-Drive",
                         task="autonomous-driving", backend="mock"))
engine = InferenceEngine(config.inference, ctx.backends)
print("模型数:", len(ctx.models))
print(engine.generate("规划"))
