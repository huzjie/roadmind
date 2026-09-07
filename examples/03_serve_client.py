"""启动服务并用 SDK 访问。"""
# 服务端：
#   roadmind --config configs/roadmind.mock.yaml serve --port 8000
# 客户端：
from roadmind.sdk.client import RoadMindClient

client = RoadMindClient("http://127.0.0.1:8000/v1")
print(client.health())
print(client.generate("前方红灯，请给指令。"))
print(client.plan())
