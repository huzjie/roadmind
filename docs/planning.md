# 规划模块

- `TrajectoryPredictor`：恒速 / 恒加速轨迹预测
- `MotionPlanner`：直行 / 变道 / 停车轨迹（五次多项式横向）
- `DecisionMaker`：规则 + 模型指令融合的高层决策
- `SafetyChecker`：TTC / 安全距离校验
- `Planner`：端到端入口（感知 → 决策 → 轨迹 → 安全）
