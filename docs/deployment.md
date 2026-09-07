# 部署

## Docker

```bash
docker build -t roadmind .
docker run -p 8000:8000 roadmind
```

## Kubernetes

```bash
kubectl apply -f deploy/k8s/deployment.yaml
```

## CI

见 `.github/workflows/ci.yml`（多 Python 版本矩阵）。
