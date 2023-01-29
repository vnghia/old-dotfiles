import shutil
import subprocess
from pathlib import Path
from typing import Optional

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

        if self.should_install:
            self.dest_file = download_to_file(
                self.url, prompt=self.prompt, suffix=self.suffix
            )


class SetupScript(SetupBase):
    def __init__(
        self,
        url: str,
        command: str,
        prompt: Optional[str] = None,
        suffix: str = ".sh",
        entry_point: Optional[str] = "sh",
    ):
        super().__init__(url, command, prompt, suffix)
        self.entry_point = entry_point

    def execute(self, *args: str, **kwargs):
        if self.should_install:
            return subprocess.run(
                ([self.entry_point] if self.entry_point else [])
                + [self.dest_file.name]
                + list(args),
                **kwargs,
            )
