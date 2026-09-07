"""跨模块共享的数据类型（dataclass）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class BoundingBox2D:
    """图像平面 2D 框（像素坐标）。"""

    x1: float
    y1: float
    x2: float
    y2: float
    label: str
    confidence: float = 1.0

    @property
    def width(self) -> float:
        return max(0.0, self.x2 - self.x1)

    @property
    def height(self) -> float:
        return max(0.0, self.y2 - self.y1)

    @property
    def area(self) -> float:
        return self.width * self.height


@dataclass
class BoundingBox3D:
    """3D 目标框（相机或自车坐标系）。"""

    cx: float
    cy: float
    cz: float
    length: float
    width: float
    height: float
    yaw: float
    label: str
    confidence: float = 1.0


@dataclass
class Detection:
    """统一检测结果。"""

    box2d: Optional[BoundingBox2D] = None
    box3d: Optional[BoundingBox3D] = None
    label: str = "unknown"
    confidence: float = 1.0
    track_id: Optional[int] = None
    velocity: Optional[Tuple[float, float]] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Lane:
    """车道线 / 车道实例。"""

    lane_id: int
    polyline: List[Tuple[float, float]]
    lane_type: str = "dashed"
    color: str = "white"
    confidence: float = 1.0


@dataclass
class TrafficLight:
    """交通灯。"""

    light_id: int
    state: str  # red / green / yellow / unknown
    box2d: Optional[BoundingBox2D] = None
    confidence: float = 1.0


@dataclass
class TrafficSign:
    """交通标志。"""

    sign_id: int
    sign_type: str
    box2d: Optional[BoundingBox2D] = None
    confidence: float = 1.0


@dataclass
class Waypoint:
    """规划路径点（自车坐标系）。"""

    x: float
    y: float
    t: float
    vx: float = 0.0
    vy: float = 0.0
    heading: float = 0.0


@dataclass
class Trajectory:
    """预测或规划轨迹。"""

    waypoints: List[Waypoint]
    confidence: float = 1.0
    source: str = "model"

    @property
    def length(self) -> int:
        return len(self.waypoints)

    @property
    def duration(self) -> float:
        if not self.waypoints:
            return 0.0
        return self.waypoints[-1].t - self.waypoints[0].t


@dataclass
class DrivingCommand:
    """高层驾驶指令。"""

    action: str  # stop / go / slow_down / turn_left / turn_right / keep_lane / change_lane
    reason: str = ""
    target_speed: Optional[float] = None
    confidence: float = 1.0


@dataclass
class VQAResult:
    """视觉问答结果。"""

    question: str
    answer: str
    confidence: float = 1.0
    raw: str = ""


@dataclass
class SceneGraph:
    """场景图：目标 + 关系。"""

    objects: List[Detection] = field(default_factory=list)
    lanes: List[Lane] = field(default_factory=list)
    lights: List[TrafficLight] = field(default_factory=list)
    signs: List[TrafficSign] = field(default_factory=list)
    relations: List[Tuple[str, str, str]] = field(default_factory=list)

    @property
    def object_count(self) -> int:
        return len(self.objects)


@dataclass
class PerceptionResult:
    """感知阶段输出。"""

    detections: List[Detection] = field(default_factory=list)
    lanes: List[Lane] = field(default_factory=list)
    lights: List[TrafficLight] = field(default_factory=list)
    signs: List[TrafficSign] = field(default_factory=list)
    scene_graph: Optional[SceneGraph] = None
    bev_features: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelCard:
    """模型注册卡。"""

    name: str
    family: str
    task: str
    backend: str
    parameter_billions: float = 0.0
    context_length: int = 0
    license: str = ""
    local: bool = False
    tags: List[str] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)
