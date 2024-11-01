from uuid import UUID, uuid4

import numpy as np


class Image:
    def __init__(self, image: np.array, uuid: UUID = None):
        if not uuid:
            self._uuid = uuid4()
        else:
            self._uuid = uuid
        self._image = image
        height, width = image.shape[:2]
        self._width = width
        self._height = height

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def image(self) -> np.array:
        return self._image

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height
