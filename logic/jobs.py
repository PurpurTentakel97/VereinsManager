# Purpur Tentakel
# 21.01.2022
# VereinsManager / Jobs

from datetime import date

from logic.members import Member

jobs: list=list()


class Material:
    def __init__(self, name: str):
        self.name: str = name
        self.count: int = int()
        self.comment_text: str = str()


class Job:
    def __init__(self, name: str):
        self.name: str = name
        self.task: str = str()
        self.dead_line: date | None = None
        self.work_date: date | None = None
        self.reminder_date: date | None = None
        self.comment_text: str = str()
        self.finished: bool = False

        self.sub_jobs: list[Job] = list()


class PersonalJob(Job):
    def __init__(self, name: str):
        super().__init__(name=name)


class WorkJob(Job):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.helper: list[Member]
        self.responsible: str = str()
        self.material: list[Material] = list()
