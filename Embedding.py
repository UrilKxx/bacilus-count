import queue
from threading import Thread, Lock
from typing import List
from uuid import UUID

import cv2
import numpy as np

from logger.logger import get_logger
from domain import ProcessedImage, Image, Job, Status
from handler import CannyHandler
from storage import Storage

logger = get_logger(__name__)


# Декоратор для многопоточного выполнения функции без ожидания завершения
def async_method(func):
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


class Embedding:
    def __init__(self, storage: Storage):
        self.storage: Storage = storage
        self.jobs = queue.Queue()  # Очередь заданий
        self.lock = Lock()  # Блокировка для синхронизации доступа к заданиям

    def add_image(self, file):
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        image = Image(img)
        with self.storage as storage:
            storage.add_image(image)

    def add_image_img(self, img: np.array, uuid: UUID):
        image = Image(img, uuid)
        with self.storage as storage:
            storage.add_image(image)

    def get_image_by_uuid(self, uuid: str) -> Image:
        uuid = UUID(uuid)
        with self.storage as storage:
            return storage.get_image_by_uuid(uuid)

    def get_processed_image(self, uuid: str) -> ProcessedImage:
        uuid = UUID(uuid)
        with self.storage as storage:
            return storage.get_processed_image_by_uuid(uuid)

    def get_list_images(self) -> List[str]:
        images = []
        with self.storage as storage:
            images.extend(storage.get_list_images())
        with self.storage as storage:
            images.extend(storage.get_list_processed_image())
        return images

    def get_list_unprocessed_images(self) -> List[str]:
        with self.storage as storage:
            return storage.get_list_images()

    def get_list_processed_images(self) -> List[str]:
        with self.storage as storage:
            return storage.get_list_processed_image()

    @async_method
    def handle_algorithm(self, uuid: str):
        uuid = UUID(uuid)
        # Получаем изображение по UUID
        try:
            with self.storage as storage:
                image = storage.get_image_by_uuid(uuid)
            # Создаём новое задание
            job = Job(Status.UNKNOWN, image)
            # Добавляем задание в очередь
            with self.lock:
                self.jobs.put(job)
            # Обрабатываем изображение через CannyHandler
            CannyHandler.handle(job=job)
            # Обновляем статус задания
            if job.status == Status.COMPLETED:
                with self.storage as storage:
                    storage.add_processed_image(job.image)
            # Удаляем задание из очереди или обновляем его статус
            with self.lock:
                pass
        except ValueError as e:
            logger.error(e.args[0])
            job = Job(Status.ERROR, cause=e.args[0])
            # Добавляем задание в очередь
            with self.lock:
                self.jobs.put(job)

    def get_jobs(self) -> List[Job]:
        """
        Возвращает список текущих заданий в очереди.
        Эта функция безопасна для многопоточного доступа.
        """
        with self.lock:
            # Извлекаем задания из очереди, не удаляя их
            jobs_list = list(self.jobs.queue)
        return jobs_list

    def get_job_by_uuid(self, uuid: str) -> Job:
        with self.lock:
            # Извлекаем задания из очереди, не удаляя их
            jobs_list = list(self.jobs.queue)
        for job in jobs_list:
            if job.uuid == UUID(uuid):
                return job
        raise ValueError(f'Job not found with UUID {uuid}')
