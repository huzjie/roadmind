"""导出默认配置为 YAML。"""
from roadmind.config.loader import load_config
from roadmind.config.schema import AppConfig
import dataclasses
import yaml
import sys


def main():
    cfg = load_config()
    print(yaml.safe_dump(dataclasses.asdict(cfg), allow_unicode=True, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
