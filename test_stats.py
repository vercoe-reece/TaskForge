from stats import calculate_xp, calc_completed_tasks, calc_task_prio_stats, calc_task_category_count, calc_completed_today, calc_xp_today, calc_most_tasks_day, calc_most_xp_day, calc_stats_this_week, calc_completion_rate
from datetime import date
from datetime import timedelta

def test_high_calculate_xp():
    assert calculate_xp("🔴 High") == 100

def test_medium_calculate_xp():
    assert calculate_xp("🟠 Medium") == 50
    
def test_low_calculate_xp():
    assert calculate_xp("🟢 Low") == 25

def test_invalid_calculate_xp():
    assert calculate_xp("Banana") == 0

def test_calc_completed_tasks():
    tasks = [
        {"completed": True},
        {"completed": False},
        {"completed": True}
    ]

    completed, remaining, total = calc_completed_tasks(tasks)

    assert completed == 2
    assert remaining == 1
    assert total == 3

def test_calc_completed_tasks_empty():

    tasks = []

    completed, remaining, total = calc_completed_tasks(tasks)

    assert completed == 0
    assert remaining == 0
    assert total == 0

def test_calc_task_prio_stats():

    tasks = [
        {"completed": False, "priority": "🔴 High"},
        {"completed": False, "priority": "🟠 Medium"},
        {"completed": False, "priority": "🟢 Low"},
        {"completed": True, "priority": "🔴 High"}
    ]
    high, medium, low = calc_task_prio_stats(tasks)

    assert high == 1
    assert medium == 1
    assert low == 1

def test_calc_task_category_count():
    tasks = [
        {"completed": False, "category": "💼 Work"},
        {"completed": False, "category": "📚 Learning"},
        {"completed": False, "category": "🏠 Personal"},
        {"completed": False, "category": "💪 Health"},
        {"completed": False, "category": "💻 Projects"},
        {"completed": True, "category": "📦 Other"}
    ]

    category_counts = calc_task_category_count(tasks)

    assert category_counts["💼 Work"] == 1
    assert category_counts["📚 Learning"] == 1
    assert category_counts["🏠 Personal"] == 1
    assert category_counts["💪 Health"] == 1
    assert category_counts["💻 Projects"] == 1
    assert category_counts["📦 Other"] == 0

def test_calc_completed_today():
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    tasks = [
        {"completed_date": today},
        {"completed_date": yesterday},
        {"completed_date": today},
        {"completed_date": ""}
    ]

    completed_today = calc_completed_today(tasks)

    assert completed_today == 2

def test_calc_xp_today():
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    tasks = [
        {"completed_date": today, "priority": "🔴 High"},
        {"completed_date": today, "priority": "🟠 Medium"},
        {"completed_date": yesterday, "priority": "🔴 High"},
        {"completed_date": today, "priority": "🟢 Low"}
    ]

    xp_today = calc_xp_today(tasks)

    assert xp_today == 175

def test_calc_most_tasks_day():
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    
    tasks = [
        {"completed_date": today},
        {"completed_date": today},
        {"completed_date": today},
        {"completed_date": yesterday},
        {"completed_date": yesterday},
        {"completed_date": ""}
    ]

    most_tasks_day = calc_most_tasks_day(tasks)

    assert most_tasks_day == 3

def test_calc_most_xp_day():
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    tasks = [
        {"completed_date": today, "priority": "🔴 High"},
        {"completed_date": today, "priority": "🔴 High"},
        {"completed_date": today, "priority": "🟢 Low"},
        {"completed_date": yesterday, "priority": "🔴 High"},
        {"completed_date": yesterday, "priority": "🔴 High"}
    ]

    most_xp_day = calc_most_xp_day(tasks)

    assert most_xp_day == 225

def test_calc_stats_this_week():
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    last_week = week_start - timedelta(days=1)

    tasks = [
        {"completed_date": str(today), "priority": "🔴 High"},
        {"completed_date": str(today), "priority": "🟠 Medium"},
        {"completed_date": str(last_week), "priority": "🔴 High"},
        {"completed_date": str(week_start), "priority": "🟢 Low"},
        {"completed_date": "", "priority": "🟠 Medium"}
    ]

    xp_this_week, completed_this_week = calc_stats_this_week(tasks)

    assert xp_this_week == 175
    assert completed_this_week == 3

def test_calc_completion_rate():
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    days_this_week = today.weekday() +1
    expected_average = round(3 / days_this_week, 1)

    tasks = [
        {"completed": True, "completed_date": str(today), "priority": "🔴 High"},
        {"completed": True, "completed_date": str(yesterday), "priority": "🔴 High"},
        {"completed": False, "completed_date": "", "priority": "🔴 High"},
        {"completed": True, "completed_date": str(today), "priority": "🔴 High"}
    ]

    completion_rate, daily_average = calc_completion_rate(tasks)

    assert completion_rate == 75
    assert daily_average == expected_average
    
def test_calc_completion_rate_empty():

    tasks = []

    completion_rate, daily_average = calc_completion_rate(tasks)

    assert completion_rate == 0
    assert daily_average == 0