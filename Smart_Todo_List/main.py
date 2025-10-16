import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Task:
    def __init__(self, title: str, priority: int = 3, deadline: Optional[str] = None, 
                 recurring: Optional[str] = None, task_id: Optional[int] = None):
        self.id = task_id if task_id else id(self)
        self.title = title
        self.priority = priority  # 1=High, 2=Medium, 3=Low
        self.deadline = deadline
        self.recurring = recurring  # daily, weekly, monthly
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = None

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'deadline': self.deadline,
            'recurring': self.recurring,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        task = Task(
            title=data['title'],
            priority=data['priority'],
            deadline=data.get('deadline'),
            recurring=data.get('recurring'),
            task_id=data['id']
        )
        task.completed = data['completed']
        task.created_at = data['created_at']
        task.completed_at = data.get('completed_at')
        return task

class TodoList:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(t) for t in data]
            except:
                self.tasks = []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add_task(self, title: str, priority: int = 3, deadline: Optional[str] = None, 
                 recurring: Optional[str] = None):
        task = Task(title, priority, deadline, recurring)
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task added: {title}")

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id and not task.completed:
                task.completed = True
                task.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Handle recurring tasks
                if task.recurring:
                    self._create_recurring_task(task)
                
                self.save_tasks()
                print(f"✓ Task completed: {task.title}")
                return
        print("✗ Task not found or already completed")

    def _create_recurring_task(self, task: Task):
        new_deadline = None
        if task.deadline:
            deadline_dt = datetime.strptime(task.deadline, "%Y-%m-%d")
            if task.recurring == "daily":
                new_deadline = (deadline_dt + timedelta(days=1)).strftime("%Y-%m-%d")
            elif task.recurring == "weekly":
                new_deadline = (deadline_dt + timedelta(weeks=1)).strftime("%Y-%m-%d")
            elif task.recurring == "monthly":
                new_deadline = (deadline_dt + timedelta(days=30)).strftime("%Y-%m-%d")
        
        new_task = Task(task.title, task.priority, new_deadline, task.recurring)
        self.tasks.append(new_task)
        print(f"  → Recurring task scheduled: {task.title}")

    def delete_task(self, task_id: int):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                title = task.title
                del self.tasks[i]
                self.save_tasks()
                print(f"✓ Task deleted: {title}")
                return
        print("✗ Task not found")

    def get_sorted_tasks(self, show_completed: bool = False) -> List[Task]:
        tasks = [t for t in self.tasks if show_completed or not t.completed]
        
        # Sort by: priority (ascending), then deadline (nearest first), then created date
        def sort_key(task):
            deadline_val = datetime.max
            if task.deadline:
                try:
                    deadline_val = datetime.strptime(task.deadline, "%Y-%m-%d")
                except:
                    pass
            return (task.priority, deadline_val, task.created_at)
        
        return sorted(tasks, key=sort_key)

    def get_reminders(self) -> List[Task]:
        today = datetime.now().date()
        reminders = []
        
        for task in self.tasks:
            if not task.completed and task.deadline:
                try:
                    deadline = datetime.strptime(task.deadline, "%Y-%m-%d").date()
                    days_left = (deadline - today).days
                    
                    if days_left < 0:
                        task.reminder_msg = f"⚠ OVERDUE by {abs(days_left)} days"
                        reminders.append(task)
                    elif days_left == 0:
                        task.reminder_msg = "🔔 DUE TODAY"
                        reminders.append(task)
                    elif days_left <= 3:
                        task.reminder_msg = f"⏰ Due in {days_left} days"
                        reminders.append(task)
                except:
                    pass
        
        return reminders

def print_tasks(tasks: List[Task], title: str = "Tasks"):
    if not tasks:
        print(f"\n{title}: None")
        return
    
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")
    
    priority_labels = {1: "HIGH", 2: "MED", 3: "LOW"}
    
    for task in tasks:
        status = "✓" if task.completed else "○"
        priority = priority_labels.get(task.priority, "LOW")
        recurring = f" 🔄 {task.recurring}" if task.recurring else ""
        deadline = f" 📅 {task.deadline}" if task.deadline else ""
        reminder = f" {task.reminder_msg}" if hasattr(task, 'reminder_msg') else ""
        
        print(f"{status} [{priority}] {task.title}{deadline}{recurring}{reminder}")
        print(f"   ID: {task.id}")
        print()

def main():
    todo = TodoList()
    
    while True:
        print("\n" + "="*70)
        print("📝 SMART TO-DO LIST")
        print("="*70)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. View Reminders")
        print("6. View Completed Tasks")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            title = input("Task title: ").strip()
            if not title:
                print("✗ Title cannot be empty")
                continue
                
            print("Priority: 1=High, 2=Medium, 3=Low")
            priority = input("Enter priority (default 3): ").strip()
            priority = int(priority) if priority in ['1', '2', '3'] else 3
            
            deadline = input("Deadline (YYYY-MM-DD, optional): ").strip()
            deadline = deadline if deadline else None
            
            recurring = input("Recurring (daily/weekly/monthly, optional): ").strip().lower()
            recurring = recurring if recurring in ['daily', 'weekly', 'monthly'] else None
            
            todo.add_task(title, priority, deadline, recurring)
            
        elif choice == "2":
            tasks = todo.get_sorted_tasks()
            print_tasks(tasks, "Active Tasks (Sorted by Priority & Deadline)")
            
        elif choice == "3":
            tasks = todo.get_sorted_tasks()
            print_tasks(tasks, "Active Tasks")
            try:
                task_id = int(input("Enter task ID to complete: "))
                todo.complete_task(task_id)
            except ValueError:
                print("✗ Invalid ID")
                
        elif choice == "4":
            tasks = todo.get_sorted_tasks()
            print_tasks(tasks, "Active Tasks")
            try:
                task_id = int(input("Enter task ID to delete: "))
                todo.delete_task(task_id)
            except ValueError:
                print("✗ Invalid ID")
                
        elif choice == "5":
            reminders = todo.get_reminders()
            print_tasks(reminders, "⏰ Reminders & Upcoming Deadlines")
            
        elif choice == "6":
            completed = [t for t in todo.tasks if t.completed]
            print_tasks(completed, "Completed Tasks")
            
        elif choice == "7":
            print("Goodbye! Stay productive! 🚀")
            break
            
        else:
            print("✗ Invalid choice")

if __name__ == "__main__":
    main()