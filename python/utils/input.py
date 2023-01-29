from __future__ import annotations

from pathlib import Path
from typing import Optional


def read_input(prompt: str, default: str, *args: str) -> str:
    user_input = (
        input(f"{prompt} ({'/'.join(args) if len(args) else default}): ") or default
    )
    print()
    return user_input


def read_path(prompt: str, default: Path) -> Path:
    path = Path(read_input(prompt, str(default)))
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_options(prompt: str, options: list[str], default: Optional[str] = None):
    default = default or options[0]
    default_idx = options.index(default)
    options = options.copy()
    options[default_idx] = options[default_idx].upper()
    return read_input(prompt, default, *options).lower()


def read_binary(prompt: str, default_true: bool = True) -> bool:
    return read_options(prompt, ["y", "n"], "y" if default_true else "n") == "y"
