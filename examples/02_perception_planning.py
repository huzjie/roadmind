"""感知 + 规划端到端示例。"""
from roadmind.config.loader import load_config
from roadmind.core.context import RuntimeContext
from roadmind.core.registry import BackendRegistry
from roadmind.inference.backends.mock_backend import MockBackend
from roadmind.inference.engine import InferenceEngine
from roadmind.perception.pipeline import PerceptionPipeline
from roadmind.planning.planner import Planner

config = load_config()
ctx = RuntimeContext(config=config)
ctx.backends.register("mock", MockBackend)
engine = InferenceEngine(config.inference, ctx.backends)

perception = PerceptionPipeline(config.perception, engine)
planner = Planner(config.planning, engine)

result = perception.run(None)
plan = planner.plan(result)
print("指令:", plan["command"].action, "|", plan["command"].reason)
print("安全:", plan["safe"], "| 航点:", plan["trajectory"].length)
