"""仿真模块测试。"""
from roadmind.simulation.simulator import Simulator
from roadmind.simulation.scenarios import free_road, leading_car


def test_free_road_no_collision():
    world, ego, obs = free_road()
    sim = Simulator(world, ego, obs)
    history = sim.run(20, accel=1.0)
    assert not history[-1].collision


def test_leading_car_collision():
    world, ego, obs = leading_car(10.0)
    sim = Simulator(world, ego, obs)
    history = sim.run(200, accel=3.0)
    assert any(h.collision for h in history)


def test_ego_kinematics():
    from roadmind.simulation.ego import EgoVehicle
    ego = EgoVehicle()
    ego.step(2.0, 0.0, 0.5)
    assert ego.speed > 0
