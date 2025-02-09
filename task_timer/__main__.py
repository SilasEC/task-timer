import click
import time
import json
import os
from task_timer.task_class import Task
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
tasks = []

TASKS_FILE = "tasks.json"

console = Console()

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
    """"Make format of time readable. """

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    return f"{hours} hours {minutes} minutes {seconds} seconds"

@click.command()
@click.argument("task_name", type=str)
def new_task(task_name):
    """Create a new task with certain name. """

    for task in tasks:
        if task.name == task_name:
            console.print("\nThere is already a task with this name.\n",style="red")
            return
    task = Task(task_name)
    tasks.append(task)
    save_tasks()  # Save tasks after creating a new task
    console.print(f'\nCreated new task "{task_name}" at {task.start_time}\n', style="green")

@click.command()
@click.argument("task_name", type=str)
def finish_task(task_name):
    """End a specified task. """
    
    for task in tasks:
        if task.name == task_name and task.end_time == "Running":
            task.end_task()
            save_tasks()  # Save tasks after finishing a task
            console.print(f'\nEnded task "{task_name}" at {task.end_time}, total time: {task.time:.2f} seconds\n', style="green")
            return
    console.print(f"\nTask with name '{task_name}' not found or already finished.\n", style="red")

@click.command()
@click.option('--current', is_flag=True, help='Print just currently running tasks.')
@click.option('--finished', is_flag=True, help='Print just finished tasks.')
def print_timesheet(current, finished):
    """Show tasks and their attributes in table."""
    
    print()
    table = Table(title="Timesheet", show_header=True, header_style="bold magenta", row_styles=["white","cyan","green", "bright_yellow"])
    table.add_column("Task Name")
    table.add_column("Start Time")
    table.add_column("End Time")
    table.add_column("Duration")
    
    if not finished:
        for task in tasks:
            if task.end_time == "Running":
                duration =format_time(time.time() - task.start)
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

@click.command()
def clear_tasks():
    """Clear all tasks from the JSON file."""

    with open(TASKS_FILE, 'w') as file:
        json.dump({}, file)  # Get errors if I leave it completely blank

    console.print("\nCleared all tasks.\n",style="red")
@click.group()
def main():
    """Main."""    
    pass

# Add the commands to the main CLI group
main.add_command(new_task)
main.add_command(finish_task)
main.add_command(print_timesheet)
main.add_command(clear_tasks)

if __name__ == '__main__':
    main() 
