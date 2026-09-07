"""SDK 客户端测试。"""
from roadmind.sdk.client import RoadMindClient


def test_client_url():
    c = RoadMindClient("http://127.0.0.1:8000/v1")
    assert c.base_url == "http://127.0.0.1:8000/v1"
