from datetime import date
from datetime import date, timedelta
from storage import load_tasks

# =========================
# TASK MANAGEMENT
# =========================

def add_task(tasks, task):

    tasks.append(task)
    print("Task added:", task["text"], task["priority"])
    print("Your task has been saved!")

def view_tasks(tasks):

    if not tasks:
        print("You dont have any tasks yet!")
        return

    print("\n📋Your tasks")
    print("----------")

    for number, task in enumerate(tasks, 1):

        if task["completed"]:
            status = "[✅]"
        else:
            status = "[🔳]"
        print(status, number, ".", task["text"], task["priority"], task["category"])
        if task["notes"]:
            print("    📝", task["notes"])
        if task["due_date"]:
            due_date = date.fromisoformat(task["due_date"])
            today = date.today()
            print("    📅 Due:", task["due_date"])
            if not task["completed"]:
                if due_date < today:
                    print("⚠  Overdue!")
                elif due_date == today:
                    print("Due Today!")

def complete_task(tasks):
    task_number = choose_task(tasks)

    if task_number is False:
        return False

    completed_task = tasks[task_number]

    if completed_task["completed"]:
        print("This task is already completed")
        return False

    completed_task["completed"] = True
    completed_task["completed_date"] = str(date.today())

    return completed_task

def delete_task(tasks):

    task_number = choose_task(tasks)

    if task_number is False:
        return False

    deleted_task = tasks.pop(task_number)
    print("Task deleted:", deleted_task["text"])
    return True

def search_tasks(tasks):
    search = input("Enter the keyword you'd like to search for: \n >>>").lower()
    found = False

    print("🖊   Search results:")
    print("---------------")

    for task in tasks:
        if search in task["text"].lower() or search in task["notes"].lower():
            if task["completed"]:
                status = "✅"
            else:
                status = "🔳"
            print(status, task["text"], task["priority"], task["category"])
            if task["notes"]:
                print("     📔", task["notes"])
            if task["due_date"]:
                print("     📅 Due:", task["due_date"])
            print()
            found = True

    if not found:
        print("No matching tasks found")

# =========================
# TASK INPUT / VALIDTATION
# =========================

def get_task():
    while True:
        task = input("Enter a task: \n>>>")
        notes = input("Add any notes associated with the task: \n>>>")
        due = get_due_date()
        priority = get_priority()
        category = get_category()
        new_task = {
            "text": task,
            "completed": False,
            "priority": priority,
            "notes": notes,
            "due_date": due,
            "category": category,
            "completed_date": ""
        }

        return new_task

def get_category(allow_blank=False):
    while True:
        category = input("Choose which category you'd like to add the task to: \n 1. 💼 Work \n 2. 📚 Learning \n 3. 🏠 Personal \n 4. 💪 Health \n 5. 💻 Projects \n 6. 📦 Other \n >>>")
        if allow_blank and not category:
            return ""

        if category == "1":
            return "💼 Work"
        elif category == "2":
            return "📚 Learning"
        elif category == "3":
            return "🏠 Personal"
        elif category == "4":
            return "💪 Health"
        elif category == "5":
            return "💻 Projects"
        elif category == "6":
            return "📦 Other"
        else:
            print("Please choose a valid number")

def get_due_date(allow_blank=False):
    while True:
        due = input("Add an optional due date for your task: \n ie: YYYY-MM-DD \n >>>")
        if allow_blank and not due:
            return ""
        try:
            date.fromisoformat(due)
            return due
        except ValueError:
            print("Please enter a valid format: YYYY-MM-DD")

def get_priority(allow_blank=False):
    while True:
        priority = input("Choose the priority of your task: \n 1. 🔴 High \n 2. 🟠 Medium \n 3. 🟢 Low \n\n>")

        if allow_blank and not priority:
            return ""

        if priority == "1":
            return "🔴 High"
        elif priority == "2":
            return "🟠 Medium"
        elif priority == "3":
            return "🟢 Low"
        else:
            print("Please choose a valid number")


# =========================
# TASK EDITING
# =========================

def get_edit_details():
    changes = {}

    task_text = input("What would you like to change this task to?")
    if task_text:
        changes["text"] = task_text
    task_notes = input("What would you like to change this task's notes to?")
    if task_notes:
        changes["notes"] = task_notes
    task_priority = get_priority(allow_blank=True)
    if task_priority:
        changes["priority"] = task_priority
    task_due_date = get_due_date(allow_blank=True)
    if task_due_date:
        changes["due_date"] = task_due_date
    task_category = get_category(allow_blank=True)
    if task_category:
        changes["category"] = task_category

    return changes

def apply_changes(task, changes):
    for key, value in changes.items():
        task[key] = value

    return task

def choose_task(tasks):

    if not tasks:
        print("You don't have any tasks yet")
        return False

    else:
        print("Your tasks:")
        for number, task in enumerate(tasks, 1):
            print(number, ".", task["text"])
    try:
        task_number = int(input("Which task would you like to choose?")) - 1
    except ValueError:
        print("Please enter a valid number")
        return False

    if 0<= task_number < len(tasks):
        return task_number
    else:
        print("Please choose a valid task")
        return False

def edit_task(tasks):
    task_number = choose_task(tasks)
    if task_number is False:
        return False

    changes = get_edit_details()
    if not changes:
        return False

    edited_task = apply_changes(tasks[task_number], changes)
    return edited_task

# ===========================
# TASK FILTERING / SORTING
# ===========================

def sort_tasks_by_priority(tasks):
    return sorted(
        tasks,
        key=lambda task: assign_priority_value(task["priority"])
    )

def sort_tasks_by_due_date(tasks):
    return sorted(
        tasks,
        key=lambda task: (task["due_date"] == "", task["due_date"])
    )

def sort_tasks_by_status(tasks):
    return sorted(
        tasks,
        key=lambda task: task["completed"]
    )

def assign_priority_value(priority):
    priority_value = {
            "🔴 High": 1,
            "🟠 Medium": 2,
            "🟢 Low": 3
        }

    return priority_value[priority]

def assign_status_value(status):
    status_value = {
        "completed": True,
        "incomplete": False
    }

    return status_value[status]

def sort_tasks_default(tasks):
    return sorted(
        tasks,
        key=lambda task: (task["completed"], task["due_date"] == "", task["due_date"], assign_priority_value(task["priority"]))
    )

def handle_view_tasks(tasks):
    sorted_tasks = sort_tasks_default(tasks)
    view_tasks(sorted_tasks)

    while True:

        sort_choice = input("Sort tasks by: \n\n 1. Due Date \n 2. Priority \n 3. Status \n 4. Default \n 5. Back \n >>>")

        if sort_choice == "1":
            sorted_by_date = sort_tasks_by_due_date(tasks)
            view_tasks(sorted_by_date)

        elif sort_choice == "2":
            sorted_by_prio = sort_tasks_by_priority(tasks)
            view_tasks(sorted_by_prio)

        elif sort_choice == "3":
            sorted_by_status = sort_tasks_by_status(tasks)
            view_tasks(sorted_by_status)

        elif sort_choice == "4":
            sorted_by_default = sort_tasks_default(tasks)
            view_tasks(sorted_by_default)

        elif sort_choice == "5":
            return

        else:
            print("Please choose a valid option")

def apply_filters(tasks, filters):
    filtered_tasks = []

    for task in tasks:
        if (
            (filters["category"] == "" or task["category"] == filters["category"])
            and (filters["priority"] == "" or task["priority"] == filters["priority"])
            and (
                filters["status"] == ""
                or task["completed"] == assign_status_value(filters["status"])
            )
        ):
            filtered_tasks.append(task)

    return filtered_tasks