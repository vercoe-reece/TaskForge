from tasks import add_task, delete_task, complete_task, search_tasks, get_edit_details, apply_changes, choose_task, edit_task
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