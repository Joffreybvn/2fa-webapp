import time
from io import BytesIO
from typing import Optional
import requests
from PIL import Image
from pyzbar.pyzbar import decode


def format_code(code: str) -> str:
    return f"{code[:3]} {code[3:]}"


def get_time_process() -> float:
    return (int(time.time()) % 30) / 29


class QRCodeDecoder:

    def __init__(self, image: Image):
        self._image: Image = image
        self._content: Optional[str] = None

    @classmethod
    def from_url(cls, image_url: str):
        image_data: bytes = requests.get(image_url).content
        image = Image.open(BytesIO(image_data))
        return cls(image)

    def _decode(self):
        content = decode(self._image)
        if content:
            self._content = content[0].data.decode()

    @property
    def content(self):
        if not self._content:
            self._decode()
        return self._content
