from tasks import add_task, delete_task, complete_task, search_tasks, get_edit_details, apply_changes, choose_task, edit_task, get_priority, get_category, get_due_date, sort_tasks_by_priority, sort_tasks_by_due_date, sort_tasks_by_status, sort_tasks_default, assign_priority_value, handle_view_tasks, apply_filters, assign_status_value
from datetime import date
from datetime import timedelta

def test_add_task():

    tasks = []

    task = {
        "text": "Test task",
        "priority": "🔴 High"
    }

    add_task(tasks, task)

    assert len(tasks) == 1
    assert tasks[0]["priority"] == "🔴 High"
    assert tasks[0]["text"] == "Test task"

def test_delete_task(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    tasks = [
        {"text": "Task one"},
        {"text": "Task two"}
    ]

    result = delete_task(tasks)

    assert result == True
    assert len(tasks) == 1
    assert tasks[0]["text"] == "Task two"

def test_delete_task_badinput(monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _: "99")

    tasks = [
        {"text": "Task one"},
        {"text": "Task two"}
    ]

    result = delete_task(tasks)

    assert result is False
    assert len(tasks) == 2
    assert tasks[0]["text"] == "Task one"
    assert tasks[1]["text"] == "Task two"

def test_delete_task_terribleinput(monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _: "banana")

    tasks = [
        {"text": "Task one"},
        {"text": "Task two"}
    ]

    result = delete_task(tasks)

    assert result is False
    assert len(tasks) == 2
    assert tasks[0]["text"] == "Task one"
    assert tasks[1]["text"] == "Task two"

def test_complete_task(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    today = date.today()

    tasks = [
        {"text": "Task one", "completed": False, "completed_date": ""},
        {"text": "Task two", "completed": False, "completed_date": ""},
        {"text": "Task three", "completed": False, "completed_date": ""}
    ]

    completed_task = complete_task(tasks)

    assert completed_task["completed"] is True
    assert completed_task["completed_date"] == str(today)
    assert completed_task["text"] == "Task one"
    assert tasks[0]["completed"] is True

def test_complete_task_badinput(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "99")

    tasks = [
        {"text": "Task one", "completed": False, "completed_date": ""},
        {"text": "Task two", "completed": False, "completed_date": ""},
        {"text": "Task three", "completed": False, "completed_date": ""}
    ]

    result = complete_task(tasks)

    assert result is False
    assert tasks[0]["completed"] is False
    assert tasks[0]["text"] == "Task one"
    assert tasks[0]["completed_date"] == ""
    assert tasks[1]["completed"] is False
    assert len(tasks) == 3

def test_complete_task_alreadycompleted(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    today = date.today()

    tasks = [
        {"text": "Task one", "completed": True, "completed_date": str(today)},
        {"text": "Task two", "completed": False, "completed_date": ""},
        {"text": "Task three", "completed": False, "completed_date": ""}
    ]

    result = complete_task(tasks)

    assert result is False
    assert tasks[0]["completed"] is True
    assert tasks[0]["completed_date"] == str(today)
    assert tasks[0]["text"] == "Task one"

def test_complete_task_terribleinput(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "banana")

    tasks = [
        {"text": "Task one", "completed": False, "completed_date": ""},
        {"text": "Task two", "completed": False, "completed_date": ""},
        {"text": "Task three", "completed": False, "completed_date": ""}
    ]

    result = complete_task(tasks)

    assert result is False
    assert tasks[0]["completed"] is False
    assert tasks[0]["text"] == "Task one"
    assert tasks[0]["completed_date"] == ""
    assert tasks[1]["completed"] is False
    assert len(tasks) == 3

def test_complete_task_emptylist():

    tasks = []

    result = complete_task(tasks)

    assert result is False
    assert len(tasks) == 0

def test_search_tasks(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "python")

    tasks = [
        {"text": "Test python functions",
         "notes": "Python ftw",
         "completed": True,
         "priority": "🔴 High",
         "due_date": "",
         "category": "💼 Work"}
    ]

    search_tasks(tasks)
    captured = capsys.readouterr()

    assert "Test python functions" in captured.out
    assert "Python ftw" in captured.out

def test_search_tasks_casematch(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "python")

    tasks = [
        {"text": "Test PyThOn functions",
         "notes": "PyThOn ftw",
         "completed": True,
         "priority": "🔴 High",
         "due_date": "",
         "category": "💼 Work"}
    ]

    search_tasks(tasks)
    captured = capsys.readouterr()

    assert "test python functions" in captured.out.lower()
    assert "python ftw" in captured.out.lower()

def test_search_tasks_no_matches(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "python")

    tasks = [
        {"text": "Doggy Dog",
         "notes": "Dogs ftw",
         "completed": True,
         "priority": "🔴 High",
         "due_date": "",
         "category": "💼 Work"}
    ]

    search_tasks(tasks)
    captured = capsys.readouterr()

    assert "No matching tasks found" in captured.out

def test_get_edit_details(monkeypatch):
    responses = iter(["New task name", "", "1", "", "", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    result = get_edit_details()

    assert result["text"] == "New task name"
    assert len(result) == 2
    assert "notes" not in result
    assert result["priority"] == "🔴 High"
    assert "category" not in result
    assert "due_date" not in result

def test_apply_changes():
    task = {
        "text": "Test",
        "notes": "Testing",
        "priority": "🔴 High"
    }
    changes = {
        "text": "Testy",
        "notes": "Tester"
    }

    result = apply_changes(task, changes)

    assert result["text"] == "Testy"
    assert result["notes"] == "Tester"
    assert result["priority"] == "🔴 High"

def test_choose_task(monkeypatch):
    tasks = [
        {"text": "Task one"},
        {"text": "Task two"}
    ]
    monkeypatch.setattr("builtins.input", lambda _: "1")

    result = choose_task(tasks)

    assert result == 0

def test_choose_task_invalid_number(monkeypatch, capsys):
    tasks = [
        {"text": "Task one"},
        {"text": "Task two"}
    ]
    monkeypatch.setattr("builtins.input", lambda _: "99")

    result = choose_task(tasks)
    captured = capsys.readouterr()

    assert "Please choose a valid task" in captured.out
    assert result is False

def test_choose_task_invalid_input(monkeypatch, capsys):
    tasks = [
        {"text": "Task one"},
        {"text": "Task two"}
    ]
    monkeypatch.setattr("builtins.input", lambda _: "banana")

    result = choose_task(tasks)
    captured = capsys.readouterr()

    assert "Please enter a valid number" in captured.out
    assert result is False

def test_choose_task_empty(capsys):
    tasks = []

    result = choose_task(tasks)
    captured = capsys.readouterr()

    assert "You don't have any tasks yet" in captured.out
    assert result is False

def test_edit_task(monkeypatch):
    tasks = [
        {
            "text": "Old task",
            "notes": "Old notes"
        }
    ]

    responses = iter([
        "1",
        "New task name",
        "New notes",
        "",
        "",
        ""
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    result = edit_task(tasks)

    assert result["text"] == "New task name"
    assert result["notes"] == "New notes"
    assert tasks[0]["text"] == "New task name"
    assert tasks[0]["notes"] == "New notes"

def test_edit_task_empty(capsys):
    tasks = []

    result = edit_task(tasks)
    captured = capsys.readouterr()

    assert result is False
    assert "You don't have any tasks yet" in captured.out

def test_edit_tasks_noinput(monkeypatch):
    tasks = [
            {
                "text": "Old task",
                "notes": "Old notes"
            }
        ]
    responses = iter([
        "1",
        "",
        "",
        "",
        "",
        ""
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    result = edit_task(tasks)

    assert result is False
    assert tasks[0]["text"] == "Old task"
    assert tasks[0]["notes"] == "Old notes"

def test_get_priority_noinput(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

    result = get_priority(allow_blank=True)

    assert result == ""

def test_get_category_noinput(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

    result = get_category(allow_blank=True)

    assert result == ""

def test_get_due_date_noinput(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

    result = get_due_date(allow_blank=True)

    assert result == ""

def test_get_category_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    result = get_category()

    assert result == "💼 Work"

def test_get_due_date_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2026-08-10")

    result = get_due_date()

    assert result == "2026-08-10"

# =====================
# SORT TESTING
# =====================

def test_sort_tasks_by_priority():
    tasks = [
        {"text": "Task one", "priority": "🟠 Medium"},
        {"text": "Task two", "priority": "🟢 Low"},
        {"text": "Task three", "priority": "🔴 High"}
    ]

    result = sort_tasks_by_priority(tasks)

    assert result == [
        {"text": "Task three", "priority": "🔴 High"},
        {"text": "Task one", "priority": "🟠 Medium"},
        {"text": "Task two", "priority": "🟢 Low"}
    ]

def test_sort_tasks_by_due_date():
    tasks = [
        {"text": "Task one", "due_date": "2026-08-10"},
        {"text": "Task two", "due_date": "2026-08-12"},
        {"text": "Task three", "due_date": ""},
        {"text": "Task four", "due_date": "2026-08-07"}
    ]

    result = sort_tasks_by_due_date(tasks)

    assert result == [
        {"text": "Task four", "due_date": "2026-08-07"},
        {"text": "Task one", "due_date": "2026-08-10"},
        {"text": "Task two", "due_date": "2026-08-12"},
        {"text": "Task three", "due_date": ""}
    ]

def test_sort_tasks_by_status():
     tasks = [
            {"text": "Task one", "completed": True},
            {"text": "Task two", "completed": False},
            {"text": "Task three", "completed": True},
            {"text": "Task four", "completed": False}
        ]

     result = sort_tasks_by_status(tasks)

     assert result == [
            {"text": "Task two", "completed": False},
            {"text": "Task four", "completed": False},
            {"text": "Task one", "completed": True},
            {"text": "Task three", "completed": True}
        ]

def test_assign_priority_value():
    result1 = assign_priority_value("🔴 High")
    result2 = assign_priority_value("🟠 Medium")
    result3 = assign_priority_value("🟢 Low")

    assert result1 == 1
    assert result2 == 2
    assert result3 == 3

def test_sort_tasks_default():
    tasks = [
            {"text": "Task one", "completed": True, "priority": "🔴 High", "due_date": "2026-08-12"},
            {"text": "Task two", "completed": False, "priority": "🟠 Medium", "due_date": "2026-08-20"},
            {"text": "Task three", "completed": False, "priority": "🔴 High", "due_date": "2026-08-20"},
            {"text": "Task four", "completed": False, "priority": "🟢 Low", "due_date": "2026-08-18"},
            {"text": "Task five", "completed": False, "priority": "🟠 Medium", "due_date": "2026-08-19"},
            {"text": "Task six", "completed": False, "priority": "🔴 High", "due_date": ""}
        ]

    result = sort_tasks_default(tasks)

    assert result == [
        {"text": "Task four", "completed": False, "priority": "🟢 Low", "due_date": "2026-08-18"},
        {"text": "Task five", "completed": False, "priority": "🟠 Medium", "due_date": "2026-08-19"},
        {"text": "Task three", "completed": False, "priority": "🔴 High", "due_date": "2026-08-20"},
        {"text": "Task two", "completed": False, "priority": "🟠 Medium", "due_date": "2026-08-20"},
        {"text": "Task six", "completed": False, "priority": "🔴 High", "due_date": ""},
        {"text": "Task one", "completed": True, "priority": "🔴 High", "due_date": "2026-08-12"}
    ]

def test_handle_view_tasks_priority_sort(monkeypatch):
    fake_tasks = [
        {"text": "Task one", "completed": False, "priority": "🔴 High", "due_date": "2026-08-20"},
        {"text": "Task two", "completed": False, "priority": "🟢 Low", "due_date": "2026-08-19"},
        {"text": "Task three", "completed": False, "priority": "🟠 Medium", "due_date": "2026-08-21"}
    ]

    displayed_lists = []
    responses = iter([
        "1",
        "2",
        "3"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    def fake_view_tasks(tasks):
        displayed_lists.append(tasks)

    monkeypatch.setattr("tasks.view_tasks", fake_view_tasks)

    handle_view_tasks(fake_tasks)

    assert displayed_lists[0] == [
        {"text": "Task two", "completed": False, "priority": "🟢 Low", "due_date": "2026-08-19"},
        {"text": "Task one", "completed": False, "priority": "🔴 High", "due_date": "2026-08-20"},
        {"text": "Task three", "completed": False, "priority": "🟠 Medium", "due_date": "2026-08-21"}
    ]

    assert displayed_lists[1] == [
        {"text": "Task one", "completed": False, "priority": "🔴 High", "due_date": "2026-08-20"},
        {"text": "Task three", "completed": False, "priority": "🟠 Medium", "due_date": "2026-08-21"},
        {"text": "Task two", "completed": False, "priority": "🟢 Low", "due_date": "2026-08-19"}
    ]

# =======================
# FILTERS TESTING
# =======================

def test_apply_filters_category():
    filters = {
        "category": "📚 Learning",
        "priority": "",
        "status": ""
    }


    tasks = [
        {"text": "Task one", "category": "📚 Learning"},
        {"text": "Task two", "category": "💼 Work"},
        {"text": "Task three", "category": ""},
        {"text": "Task Four", "category": "💪 Health"}
    ]

    result = apply_filters(tasks, filters)

    assert result == [
        {"text": "Task one", "category": "📚 Learning"}
    ]

def test_apply_filters_no_filter():
    filters = {
        "category": "",
        "priority": "",
        "status": ""
    }

    tasks = [
        {"text": "Task one", "category": "📚 Learning"},
        {"text": "Task two", "category": "💼 Work"},
        {"text": "Task three", "category": ""},
        {"text": "Task Four", "category": "💪 Health"}
    ]

    result = apply_filters(tasks, filters)

    assert result == [
        {"text": "Task one", "category": "📚 Learning"},
        {"text": "Task two", "category": "💼 Work"},
        {"text": "Task three", "category": ""},
        {"text": "Task Four", "category": "💪 Health"}
    ]

def test_apply_filters_priority():
    filters = {
        "category": "",
        "priority": "🔴 High",
        "status": ""
    }

    tasks = [
        {"text": "Task one", "priority": "🔴 High"},
        {"text": "Task two", "priority": ""},
        {"text": "Task three", "priority": "🟠 Medium"}
    ]

    result = apply_filters(tasks, filters)

    assert result == [
        {"text": "Task one", "priority": "🔴 High"}
    ]

def test_apply_filters_priority_and_category():
    filters = {
        "category": "📚 Learning",
        "priority": "🔴 High",
        "status": ""
    }

    tasks = [
        {"text": "Task one", "category": "📚 Learning", "priority": "🔴 High"},
        {"text": "Task two", "category": "📚 Learning", "priority": "🟠 Medium"},
        {"text": "Task three", "category": "💼 Work", "priority": "🔴 High"},
        {"text": "Task four", "category": "💼 Work", "priority": "🟠 Medium"},
    ]

    result = apply_filters(tasks, filters)

    assert result == [
        {"text": "Task one", "category": "📚 Learning", "priority": "🔴 High"}
    ]

def test_apply_status_value():

    result1 = assign_status_value("completed")
    result2 = assign_status_value("incomplete")

    assert result1 == True
    assert result2 == False

def test_apply_filters_status_completed():
    filters = {
        "category": "",
        "priority": "",
        "status": "completed"
    }

    tasks = [
        {"text": "Task one", "category": "📚 Learning", "priority": "🔴 High", "completed": True},
        {"text": "Task two", "category": "📚 Learning", "priority": "🟠 Medium", "completed": True},
        {"text": "Task three", "category": "💼 Work", "priority": "🔴 High", "completed": True},
        {"text": "Task four", "category": "💼 Work", "priority": "🟠 Medium", "completed": True},
    ]

    result = apply_filters(tasks, filters)

    assert result == [
        {"text": "Task one", "category": "📚 Learning", "priority": "🔴 High", "completed": True},
        {"text": "Task two", "category": "📚 Learning", "priority": "🟠 Medium", "completed": True},
        {"text": "Task three", "category": "💼 Work", "priority": "🔴 High", "completed": True},
        {"text": "Task four", "category": "💼 Work", "priority": "🟠 Medium", "completed": True},
    ]

def test_apply_filters_status_incomplete():
    filters = {
        "category": "",
        "priority": "",
        "status": "incomplete"
    }

    tasks = [
        {"text": "Task one", "category": "📚 Learning", "priority": "🔴 High", "completed": False},
        {"text": "Task two", "category": "📚 Learning", "priority": "🟠 Medium", "completed": True},
        {"text": "Task three", "category": "💼 Work", "priority": "🔴 High", "completed": False},
        {"text": "Task four", "category": "💼 Work", "priority": "🟠 Medium", "completed": True},
    ]

    result = apply_filters(tasks, filters)

    assert result == [
        {"text": "Task one", "category": "📚 Learning", "priority": "🔴 High", "completed": False},
        {"text": "Task three", "category": "💼 Work", "priority": "🔴 High", "completed": False}
    ]

def test_apply_filters_status_priority_category():
    filters = {
        "category": "💼 Work",
        "priority": "🔴 High",
        "status": "completed"
    }

    tasks = [
        {"text": "Task one", "category": "💼 Work", "priority": "🔴 High", "completed": True},
        {"text": "Task four", "category": "💼 Work", "priority": "🟠 Medium", "completed": True},
        {"text": "Task one", "category": "📚 Learning", "priority": "🔴 High", "completed": False},
        {"text": "Task two", "category": "📚 Learning", "priority": "🟠 Medium", "completed": True},
    ]

    result = apply_filters(tasks, filters)

    assert result == [
        {"text": "Task one", "category": "💼 Work", "priority": "🔴 High", "completed": True}
    ]