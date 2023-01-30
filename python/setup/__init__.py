import os
import shutil
import stat
import subprocess
import tempfile
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

        self.suffix = ("" if suffix and suffix.startswith(".") else ".") + suffix
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


class SetupPackage(SetupBase):
    def __init__(
        self,
        url: str,
        command: str,
        prompt: Optional[str] = None,
        suffix: str = ".sh",
        download_type: Literal["file", "git"] = "file",
    ):
        super().__init__(url, command, prompt, suffix)
        self.download_type = download_type

    @staticmethod
    def link_binsrc_bin(bin_dir: Path, binsrc_dir: Path, pattern: str):
        for bin in binsrc_dir.glob(pattern):
            linked_bin = bin_dir / bin.name
            linked_bin.unlink(missing_ok=True)
            print(f"Linking {bin} to {linked_bin}")
            (bin_dir / bin.name).symlink_to(bin)

    def install(
        self,
        bin_dir: Optional[Path] = None,
        dest_dir: Optional[Path] = None,
        pattern: str = "bin/*",
        skip_first_level=True,
    ):
        dest_dir = dest_dir or Path(os.environ["CODE_BINSRC"])
        bin_dir = bin_dir or Path(os.environ["CODE_BIN"])
        dest_dir.mkdir(parents=True, exist_ok=True)
        bin_dir.mkdir(parents=True, exist_ok=True)
        if not self.installed:
            if self.download_type == "file":
                self.download(self.download_type)
                if not self.suffix:
                    bin_path = bin_dir / self.command
                    print(f"Saving to {bin_path}")
                    shutil.copy(self.dest_file.name, bin_path)
                    bin_path.chmod(bin_path.stat().st_mode | stat.S_IEXEC)
                else:
                    binsrc_dir = dest_dir / self.command
                    if skip_first_level:
                        with tempfile.TemporaryDirectory() as tempdir_str:
                            tempdir = Path(tempdir_str)
                            shutil.unpack_archive(self.dest_file.name, tempdir)
                            subdir = [dir for dir in tempdir.glob("*") if dir.is_dir()][
                                0
                            ]
                            shutil.copytree(subdir, binsrc_dir, dirs_exist_ok=True)
                    else:
                        shutil.unpack_archive(self.dest_file.name, binsrc_dir)
                    self.link_binsrc_bin(bin_dir, binsrc_dir, pattern)
            print()
            self.installed = True
