print("====================")
print("     TASKFORGE      ")
print("====================")

def save_xp(total_xp):
    try:
        with open("stats.txt", "w") as file:
            file.write(str(total_xp))
    except:
        print("There was a problem saving your xp")

def load_xp():
    try:
        with open("stats.txt", "r") as file:
            rawxp = file.read()
            return (int(rawxp))
    except:
        return 0 
          
def calculate_xp(priority):

    if priority == "🔴 High":
        return 100
    elif priority ==  "🟠 Medium":
        return 50
    elif priority == "🟢 Low":
        return 25
    else:
        return 0
    
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

tasks = load_tasks()
total_xp = load_xp()

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
            total_xp += earned_xp
            save_tasks(tasks)
            save_xp(total_xp)

            print("🎉 Task completed!")
            print("⭐ +", earned_xp, "XP")
            print("⭐ Total XP:", total_xp)

        else:
            print("There was a problem completing your task")
            
        
    elif choice == "4":
        if delete_task(tasks):
            save_tasks(tasks)

    elif choice == "5":
        say_goodbye()
        break 

    else:
        print("That isn't a valid option.")


