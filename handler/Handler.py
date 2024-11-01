from abc import ABCMeta

from domain import Job


class Handler(metaclass=ABCMeta):

    @staticmethod
    def handle(job: Job):
        pass
