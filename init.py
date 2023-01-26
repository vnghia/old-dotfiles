import shutil
import subprocess
import sys
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


def generate_root_zshenv(
    dotfiles_home: Path,
    code_home: Path,
    dotfiles_sh_home: Path,
    dotfiles_zsh_home: Path,
    dotfiles_python_home: Path,
):
    zshenv_path = HOME / ".zshenv"
    zshenv_path.unlink(missing_ok=True)
    with open(zshenv_path, "w") as f:
        f.write("# AUTO GENERATED FILE. DO NOT EDIT\n\n")
        f.write(f"export ZDOTDIR={dotfiles_zsh_home}\n")
        f.write(f"export DF_HOME={dotfiles_home}\n")
        f.write(f"export CODE_HOME={code_home}\n")
        f.write(f"export DF_SH_HOME={dotfiles_sh_home}\n")
        f.write(f"export DF_ZSH_HOME={dotfiles_zsh_home}\n")
        f.write(f"export DF_PYTHON_HOME={dotfiles_python_home}\n")
    zshenv_path.chmod(0o555)


def check_and_install_zsh():
    from python.utils.download import download_as_str
    from python.utils.input import read_binary
    from python.utils.shell import get_current_shell

    zsh_path = shutil.which("zsh")
    if not zsh_path:
        if read_binary("Zsh not found. Install Zsh"):
            install_script = download_as_str(
                "https://raw.githubusercontent.com/romkatv/zsh-bin/master/install"
            )
            subprocess.check_call(["sh", "-c", install_script])
    else:
        print(f"Zsh found at {zsh_path}")

    if get_current_shell() != "zsh":
        print("Please set Zsh as default shell.")
        print(f"  (1) sudo chsh -s {zsh_path}")
        print(f"  (2) Add to .bash_profile / .bashrc / .profile")
        print(f"      export SHELL={zsh_path}")
        print(f'      [ -z "$ZSH_VERSION" ] && exec {zsh_path} -l')
        print(f"  (3) Add new terminal profile with command {zsh_path}")


def print_install_font():
    print("Please install Jetbrains Mono font.")
    print("  (1) https://github.com/JetBrains/JetBrainsMono")
    print(
        "  (2) https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/JetBrainsMono/Ligatures/Regular"
    )


def init():
    dotfiles_home = HOME / ".dotfiles"
    dotfiles_home = Path(
        input(f"Enter dotfiles home ({dotfiles_home}): ") or dotfiles_home
    )
    clone_dotfiles(DOTFILES_REPO_URL, dotfiles_home)

    sys.path.append(str(dotfiles_home))

    from python.utils.input import read_path

    code_home = read_path("Enter code home", HOME / "code")

    dotfiles_sh_home = dotfiles_home / "sh"
    dotfiles_zsh_home = dotfiles_home / "zsh"
    dotfiles_python_home = dotfiles_home / "python"

    generate_root_zshenv(
        dotfiles_home,
        code_home,
        dotfiles_sh_home,
        dotfiles_zsh_home,
        dotfiles_python_home,
    )

    check_and_install_zsh()

    print_install_font()


if __name__ == "__main__":
    init()
