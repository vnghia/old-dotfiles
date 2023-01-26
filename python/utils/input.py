from pathlib import Path


def read_input(prompt: str, default: str, *args: str) -> str:
    user_input = input(f"{prompt} ({'/'.join((default,) + args)}): ") or default
    print("")
    return user_input


def read_path(prompt: str, default: Path) -> Path:
    path = Path(read_input(prompt, str(default)))
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_binary(prompt: str) -> bool:
    return read_input(prompt, "Y", "n").lower() == "y"
