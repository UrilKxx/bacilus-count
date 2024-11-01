import json

from server import create_app
import time
from threading import Thread
from uuid import UUID

from storage import HDF5ImageStorage
from Embedding import Embedding
import cv2
from domain import Image, ProcessedImage, Job, Status

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)

    # storage = HDF5ImageStorage()
    # embedding = Embedding(storage)
    # img = cv2.imread(r"D:\current\lepidicid\dataset\train\img000000.jpg")
    # pr_img = cv2.imread(r"D:\current\lepidicid\dataset\train\img000025.jpg")
    # image = Image(img)
    # uuid = image.uuid
    # print("Successes is inevitable")
    # try:
    #     embedding.add_image_img(img, uuid)
    # except Exception as e:
    #     print(e)
    #
    # uuid = image.uuid
    uuid = UUID('58496484-5ef7-4e94-a2d9-084eba3d1bf8')
    # embedding.handle_algorithm(str(uuid))
    # flag = True
    # time.sleep(10)
    # while flag:
    #     for job in embedding.get_jobs():
    #         print(json.dumps(job.__dict__))
            # print(job.__dict__)
            # if job.status == Status.COMPLETED or job.status == Status.ERROR:
            #     flag = False
            #     break
        # print("-------------------------------------------------------")
#