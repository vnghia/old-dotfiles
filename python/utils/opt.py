from pathlib import Path


def read_input(prompt: str, default: str, *args: str) -> str:
    return input(f"{prompt} ({'/'.join((default,) + args)}): ") or default


def read_path(prompt: str, default: Path) -> Path:
    path = Path(read_input(prompt, str(default)))
    path.mkdir(parents=True, exist_ok=True)
    return path
