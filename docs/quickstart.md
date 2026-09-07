# 快速开始

## 安装

```bash
pip install -e .
# 或带依赖
pip install -e ".[server,torch]"
```

## 自检

```bash
roadmind doctor
```

## 离线运行（无需 GPU）

```bash
roadmind --config configs/roadmind.mock.yaml doctor
roadmind --config configs/roadmind.mock.yaml plan
```

## 启动服务

```bash
roadmind --config configs/roadmind.mock.yaml serve --port 8000
# 浏览器打开 http://127.0.0.1:8000/docs
```
