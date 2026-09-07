"""场景图构建。"""
from __future__ import annotations

from typing import List

from roadmind.core.types import Detection, Lane, SceneGraph


class SceneGraphBuilder:
    """把检测 + 车道线组装成场景图。"""

    def build(self, detections: List[Detection], lanes: List[Lane]) -> SceneGraph:
        graph = SceneGraph(objects=detections, lanes=lanes)
        # 简单关系推断：目标与车道间的 in_lane 关系
        for det in detections:
            if det.box2d is not None and lanes:
                graph.relations.append((det.label, "in_view", "camera"))
        return graph

    @staticmethod
    def summarize(graph: SceneGraph) -> str:
        """生成场景摘要文本（供规划器使用）。"""
        objs = ", ".join(sorted({d.label for d in graph.objects})) or "空场景"
        parts = ["目标:" + objs]
        if graph.lights:
            states = ", ".join(sorted({l.state for l in graph.lights}))
            parts.append("信号灯:" + states)
        if graph.signs:
            types = ", ".join(sorted({s.sign_type for s in graph.signs}))
            parts.append("标志:" + types)
        return "；".join(parts)
