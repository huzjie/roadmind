"""端到端流水线示例。"""
from roadmind.config.loader import load_config
from roadmind.core.context import RuntimeContext
from roadmind.core.registry import BackendRegistry
from roadmind.inference.backends.mock_backend import MockBackend
from roadmind.inference.engine import InferenceEngine
from roadmind.pipeline import DrivingPipeline

config = load_config()
ctx = RuntimeContext(config=config)
ctx.backends.register("mock", MockBackend)
engine = InferenceEngine(config.inference, ctx.backends)

pipeline = DrivingPipeline(config, engine)
result = pipeline.run(None)
print(pipeline.summarize(result))
