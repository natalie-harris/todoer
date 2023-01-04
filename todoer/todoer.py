import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
address = os.getenv("DB_ADDRESS")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

conn = mysql.connector.connect(host=address, password=password, user=username, database=database)
cursor = conn.cursor()
# Setting time zone so new entries are set in Eastern Time
cursor.execute("SET time_zone = '-05:00'")
conn.commit()

def format_date(id):
    # Selecting the specified entry and returning the formatted date from the date_created column
    date_entry = "SELECT DATE_FORMAT(date_created, '%a %m-%d-%y @ %h:%i%p') FROM todos WHERE id = "+ str(id)
    cursor.execute(date_entry)
    return (cursor.fetchone())[0]

def print_all(choice = 0):
    # Checking in case the user wanted to only see todos that were finished/unfinished
    match choice:
        case 1:
            cursor.execute("SELECT * FROM todos WHERE finished = 0")
        case 2:
            cursor.execute("SELECT * FROM todos WHERE finished = 1")
        case _:
            cursor.execute("SELECT * FROM todos")
    
    rows = cursor.fetchall()
    for row in rows:
        id, task, date, finished = row
        status = "Unfinished"
        if finished == 1:
            status = "Finished"
        # Formatted print of all selected entries
        print("%s) %s, %s - %s" % (id, task, status, format_date(id)))
        

def create_new():
    task = input("Enter the name of your task: ")
    # Inserting new task with user-specified description
    add_entry = "INSERT INTO todos (description) VALUES ('%s')" % task
    cursor.execute(add_entry)
    conn.commit()

def modify_task_name():
    print_all()
    print("")
    entry_id = input("Task id: ")
    # Check if entry exists
    cursor.execute("SELECT * FROM todos WHERE id = %s" % entry_id)
    entry = cursor.fetchone()
    if entry is None:
        print("Task ID not found. Nothing has been changed.")
        return
    new_task = input("New name for your task: ")
    # Changing description of task at specified entry
    modify_entry = "UPDATE todos SET description = '%s' WHERE id = %s" % (new_task, entry_id)
    cursor.execute(modify_entry)
    conn.commit()

def check_off_task():
    print_all(1)
    print("")
    entry_id = input("Task id: ")
    # Finding task and only setting to finished if it isn't already
    cursor.execute("SELECT * FROM todos WHERE id = %s" % entry_id)
    entry = cursor.fetchone()
    # Check if entry exists
    if entry is None:
        print("Task ID not found. Nothing has been changed.")
        return
    bool_state = entry[3]
    # If task is marked as finished
    if bool_state == 1:
        print("Task is already marked as finished! Nothing has been changed.")
        return
    # Setting 'finished' flag at specified entry
    modify_entry = "UPDATE todos SET finished = 1 WHERE id = %s" % entry_id
    cursor.execute(modify_entry)
    conn.commit()
    print("Task '%s' has been marked as finished.\n" % entry[1])

def delete_task():
    print_all()
    print("")
    entry_id = input("Task id: ")
    cursor.execute("SELECT * FROM todos WHERE id = %s" % entry_id)
    entry = cursor.fetchone()
    # Check if entry exists
    if entry is None:
        print("Task ID not found. Nothing has been changed.")
        return
    # Delete specified entry
    delete_entry = "DELETE FROM todos WHERE id = %s" % entry_id
    cursor.execute(delete_entry)
    conn.commit()

    

choice = 0
print("\nWelcome to Todoer")
while True:
    match choice:
        case 1:
            print_choice = int(input("Options\n"\
            "1. See only unfinished tasks\n"\
            "2. See only finished tasks\n"\
            "3. See all tasks\n"\
            "\nYour Choice: "))
            print_all(print_choice)
        case 2:
            create_new()
        case 3:
            modify_task_name()
        case 4:
            check_off_task()
        case 5:
            delete_task()
        case 6:
            print("Thank you for using Todoer!")
            exit()
    
    print("\nOptions\n"\
    "1. See your todo's\n"\
    "2. Create new todo\n" \
    "3. Modify a todo\n"\
    "4. Check off a todo\n"\
    "5. Delete a todo\n"\
    "6. Exit Todoer\n")

    choice = int(input("Your Choice: "))
    print("")

cursor.close()
conn.close()