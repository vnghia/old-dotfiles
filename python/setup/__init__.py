import shutil
import subprocess
from pathlib import Path
from typing import Literal, Optional

from python.utils.download import download_to_file
from python.utils.input import read_binary


class SetupBase:
    def __init__(
        self, url: str, command: str, prompt: Optional[str] = None, suffix: str = ".sh"
    ) -> None:
        self.url = url

        self.command = command
        self.prompt = prompt or command.capitalize()
        bin_path_str = shutil.which(self.command)
        self.should_install = read_binary(
            (
                f"{self.prompt} found ({bin_path_str}). "
                if bin_path_str
                else f"{self.prompt} not found. "
            )
            + f"Install {self.prompt}",
            bin_path_str is None,
        )
        self.bin_path = Path(bin_path_str) if bin_path_str else None

        self.suffix = suffix
        self.installed = False

    def download(
        self,
        download_type: Literal["file", "git"] = "file",
        dest: Optional[Path] = None,
        *args: str,
    ):
        if self.should_install:
            if download_type == "file":
                self.dest_file = download_to_file(
                    self.url, dest, self.prompt, suffix=self.suffix
                )
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                subprocess.check_call(["git", "clone", self.url, dest] + list(args))


class SetupScript(SetupBase):
    def __init__(
        self, url: str, command: str, prompt: Optional[str] = None, suffix: str = ".sh"
    ):
        super().__init__(url, command, prompt, suffix)

    def execute(self, prefix_cmd: str = "", suffix_cmd: str = "", **kwargs):
        if not self.installed:
            self.download()
            if self.should_install:
                return subprocess.run(
                    prefix_cmd.split() + [self.dest_file.name] + suffix_cmd.split(),
                    **kwargs,
                )
            self.installed = True
