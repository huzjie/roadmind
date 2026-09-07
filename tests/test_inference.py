"""推理引擎测试。"""
from roadmind.inference.cache import ResponseCache
from roadmind.inference.tokenizer import approximate_tokens, truncate_text


def test_mock_generate(mock_engine):
    out = mock_engine.generate("前方有红灯")
    assert "STOP" in out


def test_cache():
    c = ResponseCache(ttl=300)
    key = c.key("hello")
    assert c.get(key) is None
    c.put(key, "world")
    assert c.get(key) == "world"


def test_tokenizer():
    assert approximate_tokens("hello world") >= 2
    assert approximate_tokens("") == 0


def test_truncate():
    out = truncate_text("a b c d e f g h i j", 5)
    assert len(out.split()) <= 5
