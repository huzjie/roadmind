"""下载默认模型权重（需 HF 环境）。"""
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen-Drive-1.0-4B")
    ap.add_argument("--cache-dir", default=None)
    args = ap.parse_args()

    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("需要 huggingface_hub：pip install huggingface_hub")
        return 1
    path = snapshot_download(args.model, cache_dir=args.cache_dir)
    print("模型已下载到:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
