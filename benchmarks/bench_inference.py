"""Mock 后端吞吐基准。"""
import time

from roadmind.config.loader import load_config
from roadmind.core.context import RuntimeContext
from roadmind.core.registry import BackendRegistry
from roadmind.inference.backends.mock_backend import MockBackend
from roadmind.inference.engine import InferenceEngine

config = load_config()
ctx = RuntimeContext(config=config)
ctx.backends.register("mock", MockBackend)
engine = InferenceEngine(config.inference, ctx.backends)

start = time.perf_counter()
n = 1000
for _ in range(n):
    engine.generate("规划路线")
elapsed = time.perf_counter() - start
print(f"{n} 次推理耗时: {elapsed:.3f}s ({n/elapsed:.0f} req/s)")
