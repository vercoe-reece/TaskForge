from datetime import date
from datetime import date, timedelta

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

def calc_completed_tasks(tasks):
    completed_tasks = 0
    total_tasks = len(tasks)

    for task in tasks:
            if task["completed"]:
                completed_tasks += 1

    remaining_tasks = total_tasks - completed_tasks
    return completed_tasks, remaining_tasks, total_tasks

def calc_task_prio_stats(tasks):
    high_prio = 0
    medium_prio = 0
    low_prio = 0

    for task in tasks:
            if not task["completed"]:
                if task["priority"] == "🔴 High":
                    high_prio += 1
                elif task["priority"] == "🟠 Medium":
                    medium_prio += 1
                elif task["priority"] == "🟢 Low":
                    low_prio += 1

    return high_prio, medium_prio, low_prio

def calc_task_category_count(tasks):

    category_counts = {
            "💼 Work": 0,
            "📚 Learning": 0,
            "🏠 Personal": 0,
            "💪 Health": 0,
            "💻 Projects": 0,
            "📦 Other": 0
        }

    for task in tasks:
            if not task["completed"]:
                category_counts[task["category"]] += 1

    return category_counts

def calc_completed_today(tasks):
    today_string = str(date.today())
    completed_today = 0

    for task in tasks:
        if task["completed_date"] == today_string:
            completed_today += 1

    return completed_today

def calc_xp_today(tasks):
    xp_today = 0

    for task in tasks:
        if task["completed_date"] == str(date.today()):
            xp_today += calculate_xp(task["priority"])

    return xp_today
    
def calc_most_tasks_day(tasks):

    most_tasks_day = 0
    completion_dates = {}

    for task in tasks:
            if task["completed_date"]:
                if task["completed_date"] in completion_dates:
                    completion_dates[task["completed_date"]] +=1
                else:
                    completion_dates[task["completed_date"]] = 1

    for completed_date in completion_dates:
            if completion_dates[completed_date] > most_tasks_day:
                most_tasks_day = completion_dates[completed_date]

    return most_tasks_day

def calc_most_xp_day(tasks):

    most_xp_day = 0
    xp_by_date = {}

    for task in tasks:
            if task["completed_date"]:
                if task["completed_date"] in xp_by_date:
                    xp_by_date[task["completed_date"]] += calculate_xp(task["priority"])
                else:
                    xp_by_date[task["completed_date"]] = calculate_xp(task["priority"])

    for completed_date in xp_by_date:
            if xp_by_date[completed_date] > most_xp_day:
                most_xp_day = xp_by_date[completed_date]

    return most_xp_day

def calc_stats_this_week(tasks):

    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    xp_this_week = 0
    completed_this_week = 0 

    for task in tasks:        
            if task["completed_date"]:
                task_date = date.fromisoformat(task["completed_date"])
    
                if task_date >= week_start and task_date <= today:
                    completed_this_week += 1
                    xp_this_week += calculate_xp(task["priority"])

    return xp_this_week, completed_this_week

def calc_completion_rate(tasks):

    completed_tasks, _, total_tasks = calc_completed_tasks(tasks)
    _ , completed_this_week = calc_stats_this_week(tasks)
    today = date.today()
    days_this_week = today.weekday() +1

    if total_tasks > 0:
            completion_rate = completed_tasks / total_tasks * 100
            completion_rate = round(completion_rate)
            daily_average = round(completed_this_week / days_this_week, 1)
    else:
        completion_rate = 0
        daily_average = 0

    return completion_rate, daily_average

def view_stats(tasks, stats):
    
    completed_tasks, remaining_tasks, total_tasks = calc_completed_tasks(tasks)
    high_prio, medium_prio, low_prio = calc_task_prio_stats(tasks)
    category_counts = calc_task_category_count(tasks)
    completed_today = calc_completed_today(tasks)
    most_tasks_day = calc_most_tasks_day(tasks)
    xp_today = calc_xp_today(tasks)
    most_xp_day = calc_most_xp_day(tasks)
    xp_this_week, completed_this_week = calc_stats_this_week(tasks) 
    completion_rate, daily_average = calc_completion_rate(tasks)

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
