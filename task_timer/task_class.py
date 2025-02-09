import time
import datetime

now = datetime.datetime.now()
formatted_date = now.strftime("%H:%M:%S on %A, %B %d")
class Task:
    def __init__(self, name="Task"):
        self.name = name
        self.start = time.time()
        self.start_time = formatted_date
        self.end_time = "Running"
        self.time = 0

    def end_task(self):
        self.end = time.time()
        self.end_time = formatted_date
        self.time = self.end - self.start

    def to_dict(self):
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "time": self.time,
            "start_second": self.start,
        }

    @classmethod
    def from_dict(cls, task_dict):
        # Create a Task instance from a dictionary
        task = cls(task_dict["name"])
        task.start_time = task_dict["start_time"]
        task.end_time = task_dict["end_time"]
        task.time = task_dict["time"]
        task.start = task_dict["start_second"]
        return task