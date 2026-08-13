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