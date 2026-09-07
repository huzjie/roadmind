"""视觉问答示例。"""
from roadmind.config.loader import load_config
from roadmind.core.context import RuntimeContext
from roadmind.core.registry import BackendRegistry
from roadmind.inference.backends.mock_backend import MockBackend
from roadmind.inference.engine import InferenceEngine
from roadmind.vqa.scene_qa import SceneQA

config = load_config()
ctx = RuntimeContext(config=config)
ctx.backends.register("mock", MockBackend)
engine = InferenceEngine(config.inference, ctx.backends)

qa = SceneQA(engine)
res = qa.ask("画面中有什么目标？")
print(res.question, "->", res.answer)
