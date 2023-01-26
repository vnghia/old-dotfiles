import os
from pathlib import Path


def get_current_shell() -> str:
    return Path(f"/proc/{os.getppid()}/exe").resolve().name
