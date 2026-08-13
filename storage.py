import json

def load_tasks():
    try: 
        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks = json.load(file)
            return tasks

    except Exception as error:
        print("There was a problem loading your tasks:", error)
        return []

def save_tasks(tasks):
    try:
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent = 4, ensure_ascii=False)
    except Exception as error:
        print("There was a problem saving your tasks", error)

def load_stats():
    try:
        with open("stats.json", "r", encoding="utf-8") as file:
            stats = json.load(file)
    except Exception as error:
        print("There was a problem loading your stats:", error)
        return {
            "xp": 0,
            "streak": 0,
            "last_completed_date":"",
            "longest_streak": 0
        }
    return stats

def save_stats(stats):
    try:
        with open("stats.json", "w", encoding="utf-8") as file:
            json.dump(stats, file, indent=4)
    except Exception as error:
        print("There was a problem saving your stats:", error)