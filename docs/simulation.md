# 仿真模块

`roadmind/simulation` 提供 2D 运动学闭环仿真：

```python
from roadmind.simulation.simulator import Simulator
from roadmind.simulation.scenarios import leading_car

world, ego, obstacles = leading_car(30.0)
sim = Simulator(world, ego, obstacles)
history = sim.run(100, accel=2.0)
print("是否碰撞:", history[-1].collision)
```
