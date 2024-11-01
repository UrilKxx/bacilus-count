from typing import List
from uuid import UUID
from abc import ABC

import h5py

from logger.logger import get_logger
from storage import Storage

logger = get_logger(__name__)
from domain import *


class HDF5ImageStorage(Storage, ABC):
    def __init__(self, hdf5_file_path='images.hdf5'):
        self.hdf5_file_path = hdf5_file_path
        self.hdf5_file = None
        self.images_group = None
        self.processed_images_group = None

    def __enter__(self):
        self.hdf5_file = h5py.File(self.hdf5_file_path, 'a')
        if 'images' in self.hdf5_file:
            self.images_group = self.hdf5_file['images']
        else:
            self.images_group = self.hdf5_file.create_group('images')

        if 'processed_images' in self.hdf5_file:
            self.processed_images_group = self.hdf5_file['processed_images']
        else:
            self.processed_images_group = self.hdf5_file.create_group('processed_images')

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.hdf5_file.close()

    def add_image(self, image: Image):
        self.__check_image(image)
        image_dataset = self.images_group.create_dataset(str(image.uuid), data=image.image)
        logger.info(f"The image with UUID {image.uuid} has been added to the repository.")

    def __check_image(self, image: Image):
        for key in self.images_group.keys():
            if (image.image == self.images_group[key][()]).all():
                logger.error(f'The image has already been added with UUID {key}')
                raise ValueError(f'The image has already been added with UUID {key}')

    def add_processed_image(self, image: ProcessedImage):
        if str(image.uuid) in self.images_group:
            processed_image_dataset = self.processed_images_group.create_dataset(str(image.uuid),
                                                                                 data=image.image)
            processed_image_dataset.attrs['count'] = image.count
            del self.images_group[str(image.uuid)]
            logger.info(f"The processed image with UUID {image.uuid} has been added to the repository.")
        else:
            logger.error(f'Image not found with UUID {image.uuid}')
            raise ValueError(f'Image not found with UUID {image.uuid}')

    def   get_image_by_uuid(self, uuid: UUID) -> Image:
        if str(uuid) in self.images_group:
            image_dataset = self.images_group[str(uuid)]
            return Image(image_dataset[()], uuid)
        else:
            logger.error(f'Image not found with UUID {str(uuid)}')
            raise ValueError(f'Image not found with UUID {str(uuid)}')

    def get_processed_image_by_uuid(self, uuid: UUID) -> ProcessedImage:
        if str(uuid) in self.processed_images_group:
            processed_image_dataset = self.processed_images_group[str(uuid)]
            return ProcessedImage(uuid,
                                  processed_image_dataset[()],
                                  processed_image_dataset.attrs['count'])
        else:
            logger.error(f'Image not found with UUID {str(uuid)}')
            raise ValueError(f'Image not found with UUID {str(uuid)} ')

    def get_list_images(self) -> List[str]:
        return list(self.images_group.keys())

    def get_list_processed_image(self) -> List[str]:
        return list(self.processed_images_group.keys())
