import dataclasses
from typing import Union
from uuid import UUID, uuid4

from . import Status, Image, ProcessedImage

def snake_to_camel(input: str) -> str:
    # Can swap out with more sophisticated implementation if needed
    camel_cased = "".join(x.capitalize() for x in input.lower().split("_"))
    if camel_cased:
        return camel_cased[0].lower() + camel_cased[1:]
    else:
        return camel_cased

@dataclasses.dataclass
class Job(object):
    def __init__(self, status: Status, image: Image = None, cause: str = None):
        self._uuid = uuid4()
        self._status: Status = status
        self._image: Image | ProcessedImage = image
        self._cause: str = cause

    @property
    def status(self) -> Status:
        return self._status

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def image(self) -> Union[Image, ProcessedImage]:
        return self._image

    @property
    def cause(self) -> str:
        return self._cause

    def change_status(self, status: Status):
        self._status = status

    def set_image(self, image: Image):
        self._image = image

