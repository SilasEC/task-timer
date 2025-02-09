import click
import time
import datetime
import json
import os

tasks = []

# Path to the JSON file where tasks will be saved
TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, name="Task"):
        self.name = name
        self.start = time.time()
        self.start_time = datetime.datetime.now().isoformat()  # Save start time as ISO format string
        self.end_time = "Running"
        self.time = 0

    def end_task(self):
        self.end = time.time()
        self.end_time = datetime.datetime.now().isoformat()  # Save end time as ISO format string
        self.time = self.end - self.start

    def to_dict(self):
        # Convert task to dictionary for easy JSON serialization
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

def save_tasks():
    """Save all tasks to a JSON file."""
    with open(TASKS_FILE, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)

def load_tasks():
    """Load tasks from a JSON file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            task_dicts = json.load(file)
            return [Task.from_dict(task_dict) for task_dict in task_dicts]
    return []

# Load tasks when the script starts
tasks = load_tasks()

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    return f"{hours} hours {minutes} minutes {seconds} seconds"

@click.command()
@click.argument("task_name", type=str)
def new_task(task_name):
    """This is my main CLI."""
    load_tasks()
    for task in tasks:
        if task.name == task_name:
            click.echo("There is already a task with this name.")
            return
    task = Task(task_name)
    tasks.append(task)
    save_tasks()  # Save tasks after creating a new task
    click.echo(f'Created new task "{task_name}" at {task.start_time}')

@click.command()
@click.argument("task_name", type=str)
def finish_task(task_name):
    """This is my main CLI."""
    # Find the task to finish
    load_tasks()
    for task in tasks:
        if task.name == task_name and task.end_time == "Running":
            task.end_task()
            save_tasks()  # Save tasks after finishing a task
            click.echo(f'Ended task "{task_name}" at {task.end_time}, total time: {task.time:.2f} seconds')
            return
    click.echo(f"Task with name '{task_name}' not found or already finished.")

@click.command()
def print_timesheet():
    """Show all tasks and their elapsed times."""
    load_tasks()
    if not tasks:
        click.echo("No tasks found.")
        return
    for task in tasks:
        if task.end_time == "Running":
            click.echo(f"Task: {task.name}, Start Time: {task.start_time}, End Time: {task.end_time}, Duration: {format_time(time.time()-task.start)}")
        else:
            click.echo(f"Task: {task.name}, Start Time: {task.start_time}, End Time: {task.end_time}, Duration: {format_time(task.time)}")

@click.command()    
def print_running():
    """Show all tasks and their elapsed times."""
    load_tasks()
    check = 0
        
    for task in tasks:
        if task.end_time == "Running":
            click.echo(f"Task: {task.name}, Start Time: {task.start_time}, End Time: {task.end_time}, Duration: {format_time(time.time()-task.start)}")
            check = 1
    if check == 0:
        click.echo("No currently running tasks.")
        
@click.command()
def clear_tasks():
    """Clear all tasks from the JSON file and reset to an empty JSON object."""
    with open(TASKS_FILE, 'w') as file:
        json.dump({}, file)  # Write an empty JSON object "{}"
    click.echo("Cleared all tasks and reset to an empty JSON object in the tasks.json file.")

@click.group()
def main():
    """Main."""
    pass

# Add the commands to the main CLI group
main.add_command(new_task)
main.add_command(finish_task)
main.add_command(print_timesheet)
main.add_command(clear_tasks)
main.add_command(print_running)
if __name__ == '__main__':
    main()
