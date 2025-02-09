import time

class Task:
    def __init__(self, name = "Task"):
        self.name = name
        self.start = time.time()
        self.end = 0
        self.time = 0     

    def end_task(self):
        self.end = time.time()
        self.time = self.end-self.start
