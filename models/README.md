# RoadMind 模型目录

本目录存放模型注册卡（YAML），描述可接入 RoadMind 的视觉语言 / 语言模型。

| 模型 | 家族 | 任务 | 后端 | 参数 | 上下文 | License |
|---|---|---|---|---|---|---|
| Qwen/Qwen-Drive-1.0-4B | Qwen-Drive | autonomous-driving | transformers | 4B | 32K | Apache-2.0 |
| Qwen/Qwen3.8-27B | Qwen3.8 | multimodal-vqa | vllm | 27B | 131K | Apache-2.0 |
| deepseek-ai/DeepSeek-V4-Flash-Vision-Exp | DeepSeek | vision-flash | transformers | 16B | 65K | MIT |
| XHToken/Spark-X2.5-4B | Spark | edge-llm | ollama | 4B | 1M | Apache-2.0 |
| Lightricks/LTX-2.5 | LTX | video-generation | openai | — | — | custom |
| google/timesfm-3.0-pytorch | TimesFM | time-series | transformers | 0.2B | 512 | custom |
| Qwen/Qwen3.8-Flash-Next | Qwen3.8 | multimodal-flash | vllm | 8B | 32K | Apache-2.0 |
| MiniMaxAI/MiniMax-H3-Turbo | MiniMax-H3 | llm | openai | — | — | proprietary |

模型卡以 YAML 形式保存，`roadmind list` 可读取目录并注册。默认模型为 `Qwen/Qwen-Drive-1.0-4B`。
