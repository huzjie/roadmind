"""可观测性测试。"""
from roadmind.observability.metrics import Metrics


def test_metrics():
    m = Metrics()
    m.incr("requests")
    m.incr("requests", 2)
    m.observe("infer", 0.5)
    snap = m.snapshot()
    assert snap["counters"]["requests"] == 3
    assert snap["latency"]["infer"]["count"] == 1
