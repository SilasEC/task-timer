"""
SILAS CURTIS  
2/6/25  

Task Timer CLI  

This program creates a command line interface for tracking task durations.  
Users can create new tasks, finish tasks, display a timesheet, and clear all tasks.  
Task data is stored in a JSON file.  

Features:  
- Create a new task with a specified name  
- End a task  
- Display tasks in a formatted table  
- Clear all tasks  

"""

import click
import time
import json
import os
from task_timer.task import Task
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

TASKS_FILE = "tasks.json"
console = Console()
tasks = []


@click.group()
def main():
    """Main CLI command group."""


def save_tasks():
    """Save all tasks to a JSON file."""
    with open(TASKS_FILE, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)


def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            task_dicts = json.load(file)
            return [Task.from_dict(task_dict) for task_dict in task_dicts]
    return []


tasks = load_tasks()


def format_time(seconds):
    """Format time to be more readable."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours} hours {minutes} minutes {seconds} seconds"


@main.command()
@click.argument("task_name", type=str)
def new_task(task_name):
    """Create a new task with a specified name."""
    for task in tasks:
        if task.name == task_name:
            console.print("\nThere is already a task with this name.\n", style="red")
            return
    task = Task(task_name)
    tasks.append(task)
    save_tasks()
    console.print(f'\nCreated new task "{task_name}" at {task.start_time}\n', style="green")


@main.command()
@click.argument("task_name", type=str)
def finish_task(task_name):
    """End a specified task."""
    for task in tasks:
        if task.name == task_name and task.end_time == "Running":
            task.end_task()
            save_tasks()
            console.print(f'\nEnded task "{task_name}" at {task.end_time}, total time: {task.time:.2f} seconds\n', style="green")
            return
    console.print(f"\nTask with name '{task_name}' not found or already finished.\n", style="red")


@main.command()
@click.option('--current', is_flag=True, help='Print just currently running tasks.')
@click.option('--finished', is_flag=True, help='Print just finished tasks.')
def print_timesheet(current, finished):
    """Show tasks and their attributes in a table."""
    print()
    table = Table(title="Timesheet", show_header=True, header_style="bold magenta",
                  row_styles=["white", "cyan", "green", "bright_yellow"])
    table.add_column("Task Name")
    table.add_column("Start Time")
    table.add_column("End Time")
    table.add_column("Duration")

    if not finished:
        for task in tasks:
            if task.end_time == "Running":
                duration = format_time(time.time() - task.start)
                table.add_row(task.name, task.start_time, task.end_time, duration)

    if not current:
        for task in tasks:
            if task.end_time != "Running":
                duration = format_time(task.time)
                table.add_row(task.name, task.start_time, task.end_time, duration)

    if len(table.rows) == 0:
        console.print("No tasks to print.\n", style="red")
    else:
        console.print(table)


@main.command()
def clear_tasks():
    """Clear all tasks from the JSON file."""
    with open(TASKS_FILE, 'w') as file:
        json.dump({}, file)
    console.print("\nCleared all tasks.\n", style="red")


if __name__ == '__main__':
    main()
