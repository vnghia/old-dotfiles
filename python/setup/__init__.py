import subprocess
from typing import Optional

from python.utils.download import download_to_file


class SetupScript:
    def __init__(
        self,
        url: str,
        prompt: str,
        suffix: str = ".sh",
        entry_point: Optional[str] = "sh",
    ):
        self.url = url
        self.prompt = prompt
        self.suffix = ("" if suffix.startswith(".") else ".") + suffix
        self.entry_point = entry_point

        self.dest_file = download_to_file(
            self.url, prompt=self.prompt, suffix=self.suffix
        )

    def execute(self, *args: str, **kwargs):
        return subprocess.run(
            ([self.entry_point] if self.entry_point else [])
            + [self.dest_file.name]
            + list(args),
            **kwargs
        )
