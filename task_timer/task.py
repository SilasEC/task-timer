"""
Silas Curtis
2/7/25
Task Timer Module

This module defines a Task class that tracks the start and end times of a task,
records its duration, and allows saving data to a file.
"""

import time
import datetime

class Task:
    """ A class that represents a task to be timed. """
    
    def __init__(self, name="Task"):
        """Initialize a Task instance with a name and start time."""
        self.name = name
        self.start = time.time()
        now = datetime.datetime.now()
        self.start_time = now.strftime("%H:%M:%S on %A, %B %d")
        self.end_time = "Running"
        self.time = 0

    def end_task(self):
        """Mark the task as completed, record end time, and calculate duration."""
        self.end = time.time()
        now = datetime.datetime.now()
        self.end_time = now.strftime("%H:%M:%S on %A, %B %d")
        self.time = self.end - self.start

    def to_dict(self):
        """Convert the task instance to a dictionary representation."""
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "time": self.time,
            "start_second": self.start,
        }

    @classmethod
    def from_dict(cls, task_dict):
        """Create a Task instance from a dictionary representation."""
        task = cls(task_dict["name"])
        task.start_time = task_dict["start_time"]
        task.end_time = task_dict["end_time"]
        task.time = task_dict["time"]
        task.start = task_dict["start_second"]
        return task
