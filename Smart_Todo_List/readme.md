# 📝 Smart To-Do List

A feature-rich command-line to-do list application with priority-based sorting, deadline management, reminders, and recurring task support.

## ✨ Features

- **Priority-Based Sorting**: Tasks automatically sorted by priority (High/Medium/Low), deadline, and creation date
- **Deadline Management**: Set deadlines for tasks with automatic date validation
- **Smart Reminders**: Get alerts for overdue tasks, tasks due today, and upcoming deadlines (within 3 days)
- **Recurring Tasks**: Support for daily, weekly, and monthly recurring tasks
- **Persistent Storage**: All tasks saved to JSON file for persistence across sessions
- **Task Completion Tracking**: Mark tasks as complete with timestamp
- **Clean Interface**: User-friendly CLI with visual indicators and organized display

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher

### Setup
1. Clone or download the project files
2. No external dependencies required - uses only Python standard library!

```bash
python main.py
```

## 📖 Usage

### Main Menu Options

1. **Add Task**: Create a new task with optional priority, deadline, and recurrence
2. **View Tasks**: Display all active tasks sorted by priority and deadline
3. **Complete Task**: Mark a task as done (recurring tasks auto-generate next occurrence)
4. **Delete Task**: Permanently remove a task
5. **View Reminders**: See overdue tasks and upcoming deadlines
6. **View Completed Tasks**: Review your completed tasks
7. **Exit**: Save and quit the application

### Adding a Task

```
Task title: Complete project documentation
Priority: 1=High, 2=Medium, 3=Low
Enter priority (default 3): 1
Deadline (YYYY-MM-DD, optional): 2025-10-15
Recurring (daily/weekly/monthly, optional): weekly
```

### Priority Levels
- **1 = HIGH**: Urgent and important tasks
- **2 = MEDIUM**: Important but not urgent tasks
- **3 = LOW**: Nice-to-have tasks

### Recurring Tasks
- **daily**: Task repeats every day
- **weekly**: Task repeats every 7 days
- **monthly**: Task repeats every 30 days

When a recurring task is completed, a new instance is automatically created with the next deadline.

## 📋 Examples

### Example 1: Daily Task
```
Title: Morning workout
Priority: 1
Deadline: 2025-10-13
Recurring: daily
```

### Example 2: Weekly Task
```
Title: Team meeting
Priority: 2
Deadline: 2025-10-18
Recurring: weekly
```

### Example 3: One-time Task
```
Title: Submit report
Priority: 1
Deadline: 2025-10-14
Recurring: (leave empty)
```

## 🔔 Reminder System

The app automatically shows reminders for:
- **⚠ OVERDUE**: Tasks past their deadline
- **🔔 DUE TODAY**: Tasks due on current date
- **⏰ Due in X days**: Tasks due within 3 days

## 💾 Data Storage

Tasks are stored in `tasks.json` in the same directory as the script. This file is automatically created and updated. You can backup this file to preserve your tasks.

### Sample tasks.json structure:
```json
[
  {
    "id": 12345,
    "title": "Complete project",
    "priority": 1,
    "deadline": "2025-10-15",
    "recurring": null,
    "completed": false,
    "created_at": "2025-10-12 10:30:00",
    "completed_at": null
  }
]
```

## 🎯 Task Sorting Logic

Tasks are automatically sorted by:
1. **Priority** (High → Medium → Low)
2. **Deadline** (Nearest first)
3. **Creation Date** (Oldest first)

This ensures your most important and urgent tasks always appear at the top!

## 🛠️ Technical Details

- **Language**: Python 3.7+
- **Storage**: JSON file-based persistence
- **Dependencies**: None (uses standard library only)
- **File Size**: ~8KB (main.py)

## 📝 Tips for Best Use

1. **Set realistic priorities**: Not everything can be high priority
2. **Use deadlines**: They help maintain focus and urgency
3. **Review reminders daily**: Check upcoming tasks each morning
4. **Recurring tasks for habits**: Perfect for daily routines and weekly meetings
5. **Regular cleanup**: Delete or complete old tasks to keep the list manageable

## 🐛 Troubleshooting

**Issue**: Tasks not saving
- **Solution**: Ensure you have write permissions in the directory

**Issue**: Date format error
- **Solution**: Use YYYY-MM-DD format (e.g., 2025-10-15)

**Issue**: Can't find task ID
- **Solution**: View tasks first to see IDs, they're displayed below each task

## 🔮 Future Enhancements

Potential features for future versions:
- Task categories/tags
- Search and filter functionality
- Task notes and descriptions
- Export to CSV/PDF
- Multiple task lists
- Color-coded priorities

## 📄 License

Free to use and modify for personal and commercial projects.

## 🤝 Contributing

Feel free to fork, modify, and enhance this project. Suggestions and improvements are welcome!

---

**Stay productive! 🚀**