import io
import tempfile
from pathlib import Path
from typing import IO, Generator, Optional, Union
from urllib.request import urlopen


def download(url: str, prompt: Optional[str] = None) -> Generator[bytes, None, None]:
    resp = urlopen(url)
    prompt = prompt or url
    length = int(resp.getheader("content-length") or 0)
    total_size = 0
    block_size = int(max(4096, length / 100))
    while True:
        buf: bytes = resp.read(block_size)
        if not buf:
            break
        yield buf
        total_size += len(buf)
        if length:
            print(f"Downloading {prompt}: {100 * (total_size / length):.2f}%", end="\r")
        else:
            print(f"Downloading {prompt}: {total_size / 1000:.2f}KB", end="\r")
    print()
    print()


def download_to_stream(url: str, output: IO[bytes], prompt: Optional[str] = None):
    for buf in download(url, prompt):
        output.write(buf)


def download_as_bytes(url: str, prompt: Optional[str] = None) -> bytes:
    output = io.BytesIO()
    download_to_stream(url, output, prompt)
    return output.getvalue()


def download_as_str(
    url: str, prompt: Optional[str] = None, encoding: str = "utf-8"
) -> str:
    return download_as_bytes(url, prompt).decode(encoding)


def download_to_file(
    url: str,
    dest: Union[str, Path, None] = None,
    prompt: Optional[str] = None,
    **kwargs,
) -> IO[bytes]:
    dest_file = (
        tempfile.NamedTemporaryFile("wb", **kwargs)
        if not dest
        else open(dest, "wb", **kwargs)
    )
    download_to_stream(url, dest_file, prompt)
    return dest_file
