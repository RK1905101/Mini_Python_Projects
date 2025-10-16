import argparse
import json
import os

# File to store tasks
FILE_PATH = "tasks.json"


# Load tasks from a JSON file
def load_tasks():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return []


# Save tasks to a JSON file
def save_tasks(tasks):
    with open(FILE_PATH, "w") as file:
        json.dump(tasks, file, indent=4)


# Add a new task
def add_task(description):
    tasks = load_tasks()
    next_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": next_id, "description": description, "completed": False})
    save_tasks(tasks)
    print(f"✅ Task added (ID: {next_id}): {description}")


# View all tasks
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return

    done_tasks = [t for t in tasks if t["completed"]]
    not_done_tasks = [t for t in tasks if not t["completed"]]

    print("\n📝 To-Do List:")

    # Pending Task List
    print("\n🔸 Pending Tasks:")
    if not not_done_tasks:
        print("   ✅ All tasks are completed!")
    else:
        for task in not_done_tasks:
            print(f"   ID {task['id']}: {task['description']} - Not Done")

    # Completed Task List
    print("\n🔸 Completed Tasks:")
    if not done_tasks:
        print("   ❌ No tasks completed yet.")
    else:
        for task in done_tasks:
            print(f"   ID {task['id']}: {task['description']} - Done")

    print()


# Mark a task as completed
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"🎯 Task {task_id} marked as completed.")
            return
    print("⚠️ Task ID not found.")


# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"🗑️ Deleted task (ID: {task_id}) - {task['description']}")
            return
    print("⚠️ Task ID not found.")

        

# Update the description of an existing task
def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            old_desc = task["description"]
            task["description"] = new_description
            save_tasks(tasks)
            print(f"✏️ Updated task {task_id}: '{old_desc}' → '{new_description}'")
            return
    print("⚠️ Task ID not found.")


def main():
    parser = argparse.ArgumentParser(description="Simple CLI To-Do List App")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="Description of the task")

    # View
    subparsers.add_parser("view", help="View all tasks")

    # Complete
    parser_complete = subparsers.add_parser("complete", help="Mark a task as completed")
    parser_complete.add_argument("id", type=int, help="ID of the task to complete")

    # Delete
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="ID of the task to delete")

    # Update
    parser_update = subparsers.add_parser("update", help="Update an existing task")
    parser_update.add_argument("id", type=int, help="ID of the task to update")
    parser_update.add_argument("description", type=str, help="New description for the task")


    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "view":
        view_tasks()
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "update":
        update_task(args.id, args.description)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()