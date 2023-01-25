import io
from typing import BinaryIO
from urllib.request import urlopen


def download(url: str) -> bytes:
    return urlopen(url).read()


def download_as_str(url: str, encoding: str = "utf-8") -> str:
    return download(url).decode(encoding)
