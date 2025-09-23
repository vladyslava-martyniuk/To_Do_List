from db_querries_functions import create_db, Base, User, Task
from db_querries_functions import (
    create_task,
    create_user,
    get_all_tasks,
    get_all_users,
    get_all_tasks_by_user_id,
    get_user_by_id
)


if __name__ == "__main__":
    running = True
    while running:

        type_input = input("input: ")

        if type_input.lower() == "task":
            create_task("test name", "test description", "test deadline", 2)
        elif type_input.lower() == "user":
            create_user("test user name", "test password", "testemail@gmail.com")
        elif type_input.lower() == "gu":
            print(get_user_by_id(1))
        elif type_input.lower() == "at":
            print(get_all_tasks())
        elif type_input.lower() == "au":
            print(get_all_users())
        elif type_input.lower() == "t_id":
            print(get_all_tasks_by_user_id(2))
        elif type_input.lower() == "end":
            running = False
