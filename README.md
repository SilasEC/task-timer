# Task Timer

## Description
This is a simple Python-based timer that helps users track and manage tasks by recording how long they take to complete. It supports:
- Starting and stopping tasks
- Displaying the current running task
- Summarizing the time spent on tasks
- Storing task data in a JSON file for persistence
- Formatting output using the `rich` library
- Running multiple tasks concurrently

## Usage

The program includes several commands to manage tasks:

- **Create a new task**:  
  To start tracking a new task, use the command `start <task_name>`.
- **Finish an ongoing task**:  
  To stop tracking a task, use `finish-task <task_name>`.
- **View the timesheet**:  
  To see a summary of all tasks, use `print-timesheet`. You can filter the output to show only finished tasks or ongoing tasks using options `--finished` or `--current`.
- **Clear all tasks**:  
  To remove all tasks from the timesheet, use `clear-tasks`.

### Example Commands:
- Start a task named "project
  `new-task project`
  
- Finish a task named "Work on Project":  
  `finish-task project`
  
- View a summary of all tasks:  
  `print-timesheet`
  
- View only finished tasks:  
  `print-timesheet --finished`
  
- Clear all tasks:  
  `clear`

---

## Example of Running the Program

1. **Starting a task**  
   $ task-timer new-task project
   Created new task "project" at 23:58:50 on Tuesday, February 18
