# 配置说明

RoadMind 使用 YAML 配置，通过 `--config` 指定。完整字段见 `roadmind/config/defaults.yaml`。

## 关键字段

| 字段 | 说明 | 默认 |
|---|---|---|
| `inference.model.name` | 模型名称 | Qwen/Qwen-Drive-1.0-4B |
| `inference.model.backend` | 后端 | transformers |
| `inference.fallback_backends` | 回退后端链 | [mock] |
| `planning.horizon` | 规划时域（秒） | 6.0 |
| `planning.target_speed` | 目标车速（m/s） | 10.0 |
| `server.port` | 服务端口 | 8000 |

## 示例

见 `configs/` 目录下的多套配置。
