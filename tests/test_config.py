"""配置测试。"""
from roadmind.config.loader import load_config_from_dict


def test_default_config():
    cfg = load_config_from_dict({})
    assert cfg.app.name == "roadmind"
    assert cfg.planning.horizon == 6.0


def test_override_config():
    cfg = load_config_from_dict({"inference": {"model": {"backend": "mock"}}})
    assert cfg.inference.model.backend == "mock"


def test_unknown_field_ignored():
    cfg = load_config_from_dict({"not_exist": 123})
    assert cfg.app.name == "roadmind"
