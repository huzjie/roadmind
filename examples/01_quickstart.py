"""快速上手：doctor + 推理。"""
from roadmind.config.loader import load_config
from roadmind.core.context import RuntimeContext
from roadmind.core.registry import BackendRegistry
from roadmind.inference.backends.mock_backend import MockBackend
from roadmind.inference.engine import InferenceEngine

config = load_config()
ctx = RuntimeContext(config=config)
ctx.backends.register("mock", MockBackend)
engine = InferenceEngine(config.inference, ctx.backends)

print(engine.describe())
print(engine.generate("前方有行人，请给出驾驶指令。"))
