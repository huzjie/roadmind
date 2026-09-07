"""统一异常体系。"""


class RoadMindError(Exception):
    """RoadMind 所有异常的基类。"""


class ConfigError(RoadMindError):
    """配置加载或校验失败。"""


class BackendNotFoundError(RoadMindError):
    """指定的推理后端未注册或不可用。"""


class ModelLoadError(RoadMindError):
    """模型加载失败。"""


class InferenceError(RoadMindError):
    """推理执行失败。"""


class PerceptionError(RoadMindError):
    """感知（检测 / BEV / 车道线等）失败。"""


class PlanningError(RoadMindError):
    """规划（轨迹 / 决策）失败。"""


class EvaluationError(RoadMindError):
    """评测执行失败。"""
