# 🧾 CLI To-Do List

A simple, command-line based To-Do List app built with **Python**, using `argparse` for the CLI and `json` for persistent task storage.

---

## 🚀 Features
- ✅ Add new tasks  
- 👀 View all tasks 
- ✏️ Update existing tasks
- 🎯 Mark tasks as completed
- 🗑️ Delete tasks
- 💾 Save and load tasks automatically from `tasks.json` 
- 🆔 Each task has a unique, permanent ID

---

## ⚙️ Usage

Run all commands using:

```bash
todo <command> <arguments>
```

### 🧭 Commands

#### ✅ 1. Add a Task
Add a new task to the task manager.
```bash
todo add <task_name>
```

#### 👀 2. View Tasks
View all the tasks along with their status.
```bash
todo view
```

#### 🎯 3. Complete a Task
Mark a task as completed by its ID.
```bash
todo complete <task_id>
```

#### 🗑️ 4. Delete a Task
Delete a task by its ID.
```bash
todo delete <task_id>
```

#### ✏️ 5. Update a Task
Update a task for a particular ID.
```bash
todo update <task_id> <updated_task>
```

### ✨ List all the commands
```bash
todo --help
# or
todo -h
```