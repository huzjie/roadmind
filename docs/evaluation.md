# 评测

内置指标：ADE（平均位移误差）、FDE（终点位移误差）、碰撞率。

```python
from roadmind.eval.metrics import compute_ade, compute_fde
```

基准定义见 `roadmind/data/benchmarks/benchmarks.py`。
