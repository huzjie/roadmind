"""共享 fixture。"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def mock_engine():
    from roadmind.config.loader import load_config
    from roadmind.core.context import RuntimeContext
    from roadmind.core.registry import BackendRegistry
    from roadmind.inference.backends.mock_backend import MockBackend
    from roadmind.inference.engine import InferenceEngine

    config = load_config()
    ctx = RuntimeContext(config=config)
    ctx.backends.register("mock", MockBackend)
    return InferenceEngine(config.inference, ctx.backends)
