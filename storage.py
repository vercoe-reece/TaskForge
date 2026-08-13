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

def save_stats(stats):
    try:
        with open("stats.txt", "w", encoding="utf-8") as file:
            file.write(str(stats["xp"]) + "|" + str(stats["streak"]) + "|" + str(stats["last_completed_date"]) + "|" + str(stats["longest_streak"]))
    except Exception as error:
        print("There was a problem saving your xp:", error)