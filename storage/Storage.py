from abc import abstractmethod, ABCMeta
from typing import List
from uuid import UUID

from domain import *

class Storage(metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def add_image(self, image: Image):
        pass

    @abstractmethod
    def get_image_by_uuid(self, uuid: UUID) -> Image:
        pass

    @abstractmethod
    def get_list_images(self) -> List[str]:
        pass

    @abstractmethod
    def add_processed_image(self, processed_image: ProcessedImage):
        pass

    @abstractmethod
    def get_processed_image_by_uuid(self, uuid: UUID) -> ProcessedImage:
        pass

    @abstractmethod
    def get_list_processed_image(self) -> List[str]:
        pass
