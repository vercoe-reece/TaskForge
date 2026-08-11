print("====================")
print("     TASKFORGE      ")
print("====================")

from datetime import date
from datetime import date, timedelta

def save_stats(stats):
    try:
        with open("stats.txt", "w", encoding="utf-8") as file:
            file.write(str(stats["xp"]) + "|" + str(stats["streak"]) + "|" + str(stats["last_completed_date"]) + "|" + str(stats["longest_streak"]))
    except Exception as error:
        print("There was a problem saving your xp:", error)

def load_stats():
    try:
        with open("stats.txt", "r", encoding="utf-8") as file:
            rawstats = file.read()
            stats = rawstats.strip()
            parts = stats.split("|")
            if len(parts)>= 4:
                longest_streak = int(parts[3])
            else:
                longest_streak = int(parts[1])
            stripped_stat = {
                "xp": int(parts[0]),
                "streak": int(parts[1]),
                "last_completed_date": parts[2],
                "longest_streak": longest_streak
                }
            return stripped_stat
    except Exception as error:
        print("There was a problem loading your stats:", error)
        return {
            "xp": 0,
            "streak": 0,
            "last_completed_date":"",
            "longest_streak": 0
        }
          
def calculate_xp(priority):

    if priority == "🔴 High":
        return 100
    elif priority ==  "🟠 Medium":
        return 50
    elif priority == "🟢 Low":
        return 25
    else:
        return 0

def calc_streak(stats):

    today = date.today()
    yesterday = today - timedelta(days=1)

    if not stats["last_completed_date"]:
        stats["streak"] = 1
        if stats["streak"] > stats["longest_streak"]:
            stats["longest_streak"] = stats["streak"]
        stats["last_completed_date"] = str(today)
        return

    last_completed = date.fromisoformat(stats["last_completed_date"])

    if last_completed == yesterday:
        stats["streak"] += 1
        if stats["streak"] > stats["longest_streak"]:
            stats["longest_streak"] = stats["streak"] 
        stats["last_completed_date"] = str(today)
        return 

    if last_completed == today:
        return

    stats["streak"] = 1
    if stats["streak"] > stats["longest_streak"]:
        stats["longest_streak"] = stats["streak"]
    stats["last_completed_date"] = str(today)

def load_tasks():
    tasks = []
    try: 
        with open("tasks.txt", "r", encoding="utf-8") as file:
            rawtasks = file.readlines()
            for task in rawtasks:
                task = task.strip()
                parts = task.split("|")
                if len(parts)>= 4:
                    notes = parts[3]
                else:
                    notes = ""
                if len(parts)>= 5:
                    due = parts[4]
                else:
                    due = ""
                if len(parts)>= 6:
                    category = parts[5]
                else:
                    category = "📦 Other"
                if len(parts)>= 7:
                    completed_date = parts[6]
                else:
                    completed_date = ""
                stripped_task = {
                    "text": parts[0],
                    "completed": parts[1] == "True",
                    "priority": parts[2],
                    "notes": notes,
                    "due_date": due,
                    "category": category,
                    "completed_date": completed_date
                }  
                tasks.append(stripped_task)
            return tasks
    except Exception as error:
        print("There was a problem loading your tasks:", error)
        return []

def save_tasks(tasks):
    try:
        with open("tasks.txt", "w", encoding="utf-8") as file:
            for task in tasks:
                file.write(task["text"] + "|" + str(task["completed"]) + "|" + (task["priority"]) + "|" + (task["notes"]) + "|" + (task["due_date"]) + "|" + (task["category"]) + "|" + (task["completed_date"]) + "\n")
    except Exception as error:
        print("There was a problem saving your tasks", error)

def get_due_date():
    while True:
        due = input("Add an optional due date for your task: \n ie: YYYY-MM-DD \n >>>")
        if not due:
            return ""
        try:
            date.fromisoformat(due)
            return due
        except ValueError:
            print("Please enter a valid format: YYYY-MM-DD")
            
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

def get_category():
    while True:
        category = input("Choose which category you'd like to add the task to: \n 1. 💼 Work \n 2. 📚 Learning \n 3. 🏠 Personal \n 4. 💪 Health \n 5. 💻 Projects \n 6. 📦 Other")
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

def get_priority():
    while True:
        priority = input("Choose the priority of your task: \n 1. 🔴 High \n 2. 🟠 Medium \n 3. 🟢 Low \n\n>")
        if priority == "1":
            return "🔴 High"
        elif priority == "2":
            return "🟠 Medium"
        elif priority == "3":
            return "🟢 Low"
        else:
            print("Please choose a valid number")

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

def view_stats(tasks, stats):
    today_string = str(date.today())
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    total_tasks = len(tasks)
    completed_tasks = 0
    high_prio = 0
    medium_prio = 0
    low_prio = 0
    completed_today = 0
    most_tasks_day = 0
    xp_today = 0
    most_xp_day = 0
    completed_this_week = 0
    xp_this_week = 0
    days_this_week = today.weekday() +1
    xp_by_date = {}
    completion_dates = {}
    category_counts = {
        "💼 Work": 0,
        "📚 Learning": 0,
        "🏠 Personal": 0,
        "💪 Health": 0,
        "💻 Projects": 0,
        "📦 Other": 0
    }

    for task in tasks:
        if task["completed"]:
            completed_tasks += 1
        if not task["completed"]:
            if task["priority"] == "🔴 High":
                high_prio += 1
            elif task["priority"] == "🟠 Medium":
                medium_prio += 1
            elif task["priority"] == "🟢 Low":
                low_prio += 1
            category_counts[task["category"]] += 1
        if task["completed_date"] == today_string:
            completed_today += 1
            xp_today += calculate_xp(task["priority"])
        if task["completed_date"]:
            if task["completed_date"] in completion_dates:
                completion_dates[task["completed_date"]] +=1
            else:
                completion_dates[task["completed_date"]] = 1
        if task["completed_date"]:
            if task["completed_date"] in xp_by_date:
                xp_by_date[task["completed_date"]] += calculate_xp(task["priority"])
            else:
                xp_by_date[task["completed_date"]] = calculate_xp(task["priority"])
        if task["completed_date"]:
            task_date = date.fromisoformat(task["completed_date"])

            if task_date >= week_start and task_date <= today:
                completed_this_week += 1
                xp_this_week += calculate_xp(task["priority"])
        
    for completed_date in xp_by_date:
        if xp_by_date[completed_date] > most_xp_day:
            most_xp_day = xp_by_date[completed_date]

    for completed_date in completion_dates:
        if completion_dates[completed_date] > most_tasks_day:
            most_tasks_day = completion_dates[completed_date]
            
    remaining_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        completion_rate = completed_tasks / total_tasks * 100
        completion_rate = round(completion_rate)
        daily_average = round(completed_this_week / days_this_week, 1)
    else:
        completion_rate = 0

    print("📊 TaskForge Stats:")
    print("===============================")
    print("⭐ Total XP:", stats["xp"])
    print("🔥 Current Streak:", stats["streak"])
    print("💯 Longest Streak:", stats["longest_streak"])

    if total_tasks > 0:
        print("✅ Tasks Completed:", completed_tasks)
        print("📓 Tasks Remaining:", remaining_tasks)
        print("📈 Completion Rate:", str(completion_rate) + "%")
        print("==================")
        print("📅 Today")
        print("📅 Tasks Completed Today:", completed_today)
        print("📑 Most Tasks In One Day:", most_tasks_day)
        print("⭐ XP Earned Today:", xp_today)
        print("💰 Most XP In One Day:", most_xp_day)
        print("📊 Daily Average:", daily_average, "tasks")
        print("==================")
        print("📆 This Week")
        print("👀 XP Earned This Week:", xp_this_week)
        print("📈 Tasks Completed This Week:", completed_this_week)
        print("==================")
        print("🎯 Priorities")
        print("🔴 High Remaining:", high_prio)
        print("🟠 Medium Remaining:", medium_prio)
        print("🟢 Low Remaining:", low_prio)
        print("==================")
        print("📦 Categories")
        for category in category_counts:
            print(category, category_counts[category])

    else:
        print("😢 No task stats available")

def complete_task(tasks):

    if not tasks:
        print("You don't have any tasks yet")
        return False

    else:
        print("Your tasks:")
        for number, task in enumerate(tasks, 1 ):
            print(number, ".", task["text"])
        try:
            task_number = int(input("Which task would you like to complete?")) - 1
        except ValueError:
            print("Please choose a valid number")
            return False

        if 0 <= task_number <len(tasks):
            completed_task = tasks[task_number]
            if completed_task["completed"]:
                print("This task is already completed")
                return False

            completed_task["completed"] = True
            completed_task["completed_date"] = str(date.today())
            return completed_task

        print("Please choose a valid task")
        return False
    
def delete_task(tasks):

    if not tasks:
        print("You don't have any tasks yet")
        return False

    else:
        print("Your tasks:")
        for number, task in enumerate(tasks, 1):
            print(number, ".", task["text"])
        try:
            task_number = int(input("Which task would you like to delete?")) - 1
        except ValueError:
            print("Please enter a valid number")
            return False
        
        if 0 <= task_number < len(tasks):
            deleted_task = tasks.pop(task_number)
            print("Task deleted:", deleted_task["text"])
            return True
        else:
            print("Please choose a valid task")
            return False

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
  
def say_goodbye():

    print("Goodbye!")

stats = load_stats()
tasks = load_tasks()

while True:

    print("1. Add Task")
    print("2. View Tasks")
    print("3. View Stats")
    print("4. Search Tasks")
    print("5. Complete Task")
    print("6. Delete Task")
    print("7. Exit")

    choice = input("Choose an option:")

    if choice == "1":
        task = get_task()
        add_task(tasks, task)
        save_tasks(tasks)
        
    elif choice == "2":
        view_tasks(tasks)

    elif choice == "3":
        view_stats(tasks, stats)

    elif choice == "4":
        search_tasks(tasks)

    elif choice == "5":
        completed_task = complete_task(tasks)

        if completed_task:
            earned_xp = calculate_xp(completed_task["priority"])
            stats["xp"] += earned_xp
            calc_streak(stats)
            save_tasks(tasks)
            save_stats(stats)
            
            print("🎉 Task completed!")
            print("⭐ +", earned_xp, "XP")
            print("⭐ Total XP:", stats["xp"])
            print("🔥 Current Streak:", stats["streak"])    
        
    elif choice == "6":
        if delete_task(tasks):
            save_tasks(tasks)

    elif choice == "7":
        say_goodbye()
        break 

    else:
        print("That isn't a valid option.")