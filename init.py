import subprocess
from pathlib import Path

HOME = Path.home()
DOTFILES_REPO_URL = "https://github.com/vnghia/dotfiles.git"


def clone_dotfiles(dotfiles_repo_url: str, dotfiles_home: Path):
    dotfiles_home.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["git", "init"], cwd=dotfiles_home)
    subprocess.check_call(["git", "switch", "-C", "main"], cwd=dotfiles_home)
    subprocess.run(["git", "remote", "rm", "origin"], cwd=dotfiles_home)
    subprocess.check_call(
        ["git", "remote", "add", "origin", dotfiles_repo_url], cwd=dotfiles_home
    )
    subprocess.check_call(["git", "pull", "origin", "main"], cwd=dotfiles_home)


def init():
    dotfiles_home = HOME / ".dotfiles"
    dotfiles_home = Path(
        input(f"Enter dotfiles home ({dotfiles_home}): ") or dotfiles_home
    )
    clone_dotfiles(DOTFILES_REPO_URL, dotfiles_home)


if __name__ == "__main__":
    init()
