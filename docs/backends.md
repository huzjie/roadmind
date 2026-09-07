# 推理后端

| 后端 | 说明 | 依赖 |
|---|---|---|
| transformers | 本地 HF pipeline | torch, transformers |
| vllm | 高吞吐批量 | vllm |
| ollama | 本地 Ollama 服务 | Ollama 运行中 |
| openai | OpenAI 兼容端点 | 无 |
| mock | 离线确定性输出 | 无 |

后端通过 `roadmind.core.registry.BackendRegistry` 注册，`InferenceEngine` 按配置加载主后端，失败时依次回退。
