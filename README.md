# To-Do List App
 
A simple desktop to-do list application built with Python and Tkinter.
 
## Requirements
 
- Python 3.x
- No external libraries needed — only the Python standard library is used
## How to Run
 
```
python main.py
```
 
## Features
 
- Add tasks with a name, priority level, and optional due date
- Mark tasks as done or undone by selecting them and clicking Toggle Done, or by double-clicking
- Delete individual tasks with a confirmation prompt
- Clear all completed tasks at once
- View full details of a task (status, priority, due date, date added)
- Filter tasks by All, Active, or Done
- Live search to filter tasks by name as you type
- Color-coded list entries by priority (red for High, orange for Medium, green for Low)
- Tasks are sorted by priority, with completed tasks moved to the bottom
- Data is saved automatically to a local `tasks.json` file and reloaded on next launch
## File Structure
 
```
project/
    main.py        - main application code
    tasks.json     - auto-generated file where tasks are saved
    README.md      - this file
```
 
## Extra Features
 
1. Priority dropdown using `ttk.Combobox` with three levels: High, Medium, and Low
2. Due date field with format validation (YYYY-MM-DD)
3. Color coding using `listbox.itemconfig()` based on task priority
4. Live search that filters the task list as you type
5. Task info popup showing all stored details for a selected task
