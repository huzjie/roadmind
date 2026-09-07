# Python SDK

```python
from roadmind.sdk.client import RoadMindClient

client = RoadMindClient("http://127.0.0.1:8000/v1")
client.health()
client.generate("前方红灯，请给指令。")
client.plan()
```
