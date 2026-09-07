"""闭环仿真示例。"""
from roadmind.simulation.simulator import Simulator
from roadmind.simulation.scenarios import leading_car

world, ego, obstacles = leading_car(30.0)
sim = Simulator(world, ego, obstacles)
history = sim.run(200, accel=2.0)
print("步数:", len(history))
print("是否碰撞:", history[-1].collision)
print("是否驶出道路:", history[-1].off_road)
print("终点速度:", history[-1].ego[3])
