# Purpur Tentakel
# 21.01.2022
# VereinsManager / Jobs

from datetime import date

from logic.members import Member
from logic.enum_sheet import DateType

import transition

jobs: list = list()


class Material:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.count: int = int()
        self.comment_text: str = str()

    def set_name(self, name_: str) -> None:
        self.name: str = name_

    def set_count(self, count_: int) -> None:
        self.count: int = count_

    def set_comment_text(self, text_: str) -> None:
        self.comment_text: str = text_


class Job:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.task: str = str()
        self.dead_line: date | None = None
        self.work_date: date | None = None
        self.reminder_date: date | None = None
        self.comment_text: str = str()
        self.finished: bool = False

        self.sub_jobs: list[Job] = list()

    def set_name(self, name: str) -> None:
        self.name: str = name

    def set_task(self, task: str) -> None:
        self.task: str = task

    def set_date(self, date_type: DateType, date_: dict[str, int]) -> None:
        new_date: date = date(date_["year"], date_["month"], date_["day"])
        match date_type:
            case DateType.DEAD_LINE:
                self.dead_line: date = new_date
            case DateType.WORK_DATE:
                self.work_date: date = new_date
            case DateType.REMINDER_DATE:
                self.reminder_date: date = new_date

    def set_comment_text(self, text: str) -> None:
        self.comment_text: str = text

    def set_finished(self, finished: bool) -> None:
        self.finished: bool = finished

    def delete_sub_job(self, name: str) -> None:
        sub_job = self._get_sub_job_from_name(name=name)
        if sub_job is not None:
            self.sub_jobs.remove(sub_job)
        else:
            transition.set_window_massage("Zu löschender Sub-Job nicht vorhanden.")

    def _get_sub_job_from_name(self, name: str) -> "Job" or None:
        for sub_job in self.sub_jobs:
            if sub_job.name == name:
                return sub_job
        return None


class PersonalJob(Job):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)

    def add_sub_job(self, name: str) -> None:
        new_sub_job: PersonalJob = PersonalJob(name=name)
        self.sub_jobs.append(new_sub_job)


class WorkJob(Job):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self.helper: list[Member] = list()
        self.responsible: Member | None = None
        self.material: list[Material] = list()

    def add_helper(self, helper_: Member) -> None:
        self.helper.append(helper_)

    def remove_helper(self, helper_: Member) -> None:
        if helper_ in self.helper:
            self.helper.remove(helper_)
        else:
            transition.set_window_massage("Zu löschender Helfer nicht vorhanden.")

    def set_responsible(self, member_: Member) -> None:
        self.responsible: Member = member_

    def add_material(self, material_: Material) -> None:
        self.material.append(material_)

    def remove_material(self, material_: Material) -> None:
        if material_ in self.material:
            self.material.remove(material_)
        else:
            transition.set_window_massage("zu läschendes Material nicht vorhanden.")

    def add_sub_job(self, name: str) -> None:
        new_sub_job: WorkJob = WorkJob(name=name)
        self.sub_jobs.append(new_sub_job)
