from uuid import UUID

from . import  Image
import numpy as np


class ProcessedImage(Image):
    def __init__(self, uuid: UUID, processed_image: np.array, count):
        super().__init__(processed_image, uuid)
        self._count = count

    @property
    def count(self) -> int:
        return self._count

    def set_count(self, count: int):
        self._count = count