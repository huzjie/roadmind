"""配置加载器：YAML 文件 / 字典 -> AppConfig。"""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from roadmind.config.schema import AppConfig
from roadmind.core.exceptions import ConfigError


def _apply(target: Any, data: Dict[str, Any]) -> Any:
    """把字典递归应用到 dataclass 实例上（忽略未知字段）。"""
    for name, value in data.items():
        if not hasattr(target, name):
            continue
        current = getattr(target, name)
        if is_dataclass(current) and isinstance(value, dict):
            _apply(current, value)
        else:
            setattr(target, name, value)
    return target


def load_config_from_dict(data: Dict[str, Any]) -> AppConfig:
    """从字典构建并校验配置。"""
    if not isinstance(data, dict):
        raise ConfigError("配置必须是字典/映射，实际类型：" + type(data).__name__)
    cfg = AppConfig()
    _apply(cfg, data)
    return cfg


def load_config(path: Optional[str] = None) -> AppConfig:
    """从 YAML 文件加载配置；path 为空时使用内置默认。"""
    import yaml

    if not path:
        return AppConfig()

    p = Path(path)
    if not p.exists():
        raise ConfigError("配置文件不存在：" + str(p))

    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:  # type: ignore
        raise ConfigError("YAML 解析失败：" + str(exc)) from exc

    return load_config_from_dict(raw)
