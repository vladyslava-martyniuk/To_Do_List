from base import Base, create_db, drop_db, Session

from models.user import User
from models.task import Task


def create_task(name, description, deadline, user_id):
    with Session() as session:
        task = Task(
            name=name,
            description=description,
            deadline=deadline,
            user_id=user_id,
        )
        session.add(task)
        session.commit()
    return task


def create_user(login, password, email):
    with Session() as session:
        user = User(
            login=login,
            password=password,
            email=email,
        )
        session.add(user)
        session.commit()
    return user


def get_all_tasks():
    with Session() as session:
        all_tasks = session.query(Task).all()
        if all_tasks:
            return all_tasks
        return None


def get_all_users():
    with Session() as session:
        all_users = session.query(User).all()
        if all_users:
            return all_users
        return None


def get_task_by_id(task_id):
    with Session() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            return task
        return None


def get_user_by_id(user_id):
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return user
        return None


def get_all_tasks_by_user_id(user_id):
    with Session() as session:
        all_tasks_by_user_id = session.query(Task).filter(Task.user_id == user_id).all()
    return all_tasks_by_user_id


def update_task(task_id, name, description, deadline):
    with Session() as session:
        task = get_task_by_id(task_id)

        if not task:
            return None

        if name:
            task.name = name
        if description:
            task.description = description
        if deadline:
            task.deadline = deadline

        session.commit()
        return task


def delete_user(user_id):
    with Session() as session:
        user = get_user_by_id(user_id)
        session.delete(user)
        session.commit()


def delete_task(task_id):
    with Session() as session:
        task = get_task_by_id(task_id)
        session.delete(task)
        session.commit()
