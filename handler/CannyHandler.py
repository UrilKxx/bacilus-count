import time

from logger.logger import get_logger
from . import Handler
from domain import *

import cv2
import numpy as np
import math

logger = get_logger(__name__)

def _near_finder(set_centers, c_x, c_y):
    for set_center in set_centers:
        if 5 >= math.sqrt((c_x - set_center[0]) ** 2 + (c_y - set_center[1]) ** 2) > 0:
            return set_center
    return None


def _canny(img: np.ndarray):
    # Создание объекта CLAHE
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(2, 2))

    # Применение CLAHE на L-канале цветового пространства LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge((l_clahe, a, b))
    img_clahe = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    img_clahe = cv2.convertScaleAbs(img_clahe, alpha=2.5, beta=3)

    gray = cv2.cvtColor(img_clahe, cv2.COLOR_BGR2GRAY)
    min_val = np.min(gray)
    max_val = np.max(gray)
    # Применение детектора границ Кэнни
    threshold1 = int(max_val / 2)  # Нижний порог
    threshold2 = int(min_val * 2)  # Верхний порог
    edges = cv2.Canny(gray, threshold1, threshold2, L2gradient=True)

    # Применение операции расширения для сглаживания и закругления границ
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1, 1))
    edges_dilated = cv2.dilate(edges, kernel, iterations=50)

    # Применение операции эрозии
    edges_eroded = cv2.erode(edges_dilated, kernel, iterations=50)

    # Применение операции открытия
    edges_opened = cv2.morphologyEx(edges_eroded, cv2.MORPH_OPEN, kernel)

    # Применение операции закрытия
    edges_closed = cv2.morphologyEx(edges_opened, cv2.MORPH_CLOSE, kernel)

    # Применение операции битового ИЛИ для выделения границ на оригинальном изображении
    edges_on_original = cv2.bitwise_or(img, img, mask=edges_closed)

    # Поиск контуров на изображении с расширенными границами
    contours, hierarchy = cv2.findContours(edges_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Список для хранения областей контуров
    areas = [cv2.contourArea(cnt) for cnt in contours]
    if len(areas) == 0:
        return None
    avg_area = sum(areas) / len(areas)

    # Список для хранения координат центров
    centers = []
    # Цикл по контурам
    for cnt in contours:
        # Вычисление области контура
        area = cv2.contourArea(cnt)

        # Игнорировать слишком маленькие / большие контуры
        if area > avg_area - avg_area / 1.5:
            # avg_area + avg_area / 1.5 >
            # Вычисление моментов контура
            M = cv2.moments(cnt)
            # Вычисление координат центра контура
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                # Если момент m00 равен 0, контур является линией или точкой
                cX, cY = 0, 0

            centers.append((cX, cY))

    return centers


def _get_centers(img: np.ndarray):
    centers = _canny(img)
    if centers is None:
        return None
    set_centers = sorted(set(centers))
    for cX, cY in set_centers:
        find_near = _near_finder(set_centers, cX, cY)
        if not find_near is None:
            set_centers.remove(find_near)
    for cX, cY in centers:
        cv2.circle(img, (cX, cY), 3, (0, 150, 15), -1)
    return img, len(set_centers)


class CannyHandler(Handler):
    @staticmethod
    def handle(job: Job):
        try:
            logger.info(f"Start RUNNING job by {__name__}")
            job.change_status(Status.RUNNING)
            # img, count = _get_centers(job.image.image)
            time.sleep(10)
            job.change_status(Status.COMPLETED)
            logger.info(f"Job COMPLETED")
            job.set_image(ProcessedImage(job.image.uuid, job.image.image, 365))
        except Exception as e:
            logger.error(f"Job ERROR {e}")
            job.change_status(Status.ERROR)
