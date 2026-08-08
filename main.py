print("====================")
print("     TASKFORGE      ")
print("====================")

from datetime import date
from datetime import date, timedelta

def save_stats(stats):
    try:
        with open("stats.txt", "w", encoding="utf-8") as file:
            file.write(str(stats["xp"]) + "|" + str(stats["streak"]) + "|" + str(stats["last_completed_date"]))
    except Exception as error:
        print("There was a problem saving your xp:", error)

def load_stats():
    try:
        with open("stats.txt", "r", encoding="utf-8") as file:

            rawstats = file.read()
            stats = rawstats.strip()
            parts = stats.split("|")
            stripped_stat = {
                "xp": int(parts[0]),
                "streak": int(parts[1]),
                "last_completed_date": parts[2]
                }
            return stripped_stat
    except Exception as error:
        print("There was a problem loading your stats:", error)
        return {
            "xp": 0,
            "streak": 0,
            "last_completed_date":""
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
        stats["last_completed_date"] = str(today)
        return

    last_completed = date.fromisoformat(stats["last_completed_date"])

    if last_completed == yesterday:
        stats["streak"] += 1 
        stats["last_completed_date"] = str(today)
        return 

    if last_completed == today:
        return

    stats["streak"] = 1
    stats["last_completed_date"] = str(today)


def load_tasks():
    tasks = []
    try: 
        with open("tasks.txt", "r", encoding="utf-8") as file:
            rawtasks = file.readlines()
            for task in rawtasks:
                task = task.strip()
                parts = task.split("|")
                stripped_task = {
                    "text": parts[0],
                    "completed": parts[1] == "True",
                    "priority": parts[2]
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
                file.write(task["text"] + "|" + str(task["completed"]) + "|" + (task["priority"]) + "\n")
    except Exception as error:
        print("There was a problem saving your tasks", error)

def get_task():
    while True:
        task = input("Enter a task: \n>>>")
        priority = get_priority()
        new_task = {
            "text": task,
            "completed": False,
            "priority": priority
        }

        return new_task

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
        print(status, number, ".", task["text"], task["priority"])

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
    
def say_goodbye():

    print("Goodbye!")

stats = load_stats()
tasks = load_tasks()

while True:

    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Choose an option:")

    if choice == "1":
        task = get_task()
        add_task(tasks, task)
        save_tasks(tasks)
        
    elif choice == "2":
        view_tasks(tasks)

    elif choice == "3":
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
        
    elif choice == "4":
        if delete_task(tasks):
            save_tasks(tasks)

    elif choice == "5":
        say_goodbye()
        break 

    else:
        print("That isn't a valid option.")