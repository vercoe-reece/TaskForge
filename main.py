print("====================")
print("     TASKFORGE      ")
print("====================")

from storage import load_tasks, save_tasks, load_stats, save_stats
from stats import calculate_xp, calc_streak, view_stats 
from tasks import add_task, view_tasks, search_tasks, complete_task, delete_task, get_task

# =======================
# UI 
# =======================

def say_goodbye():

    print("Goodbye!")

# =======================
# MAIN PROGRAM
# =======================

stats = load_stats()
tasks = load_tasks()

def main():

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

if __name__ == "__main__":
    main()