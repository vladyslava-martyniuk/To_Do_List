from flask import Flask, render_template, request, redirect, url_for, session
from base import create_db, SessionLocal
from models.user import User
from models.task import Task
import hashlib
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_that_is_long_and_random"

# ------------------- Створюємо таблиці -------------------
create_db()

# ------------------- Хешування пароля -------------------
def create_password_hash(password: str):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt.hex() + ":" + key.hex()

def check_password_hash(password: str, stored: str):
    salt_hex, key_hex = stored.split(":")
    salt = bytes.fromhex(salt_hex)
    key = bytes.fromhex(key_hex)
    new_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return new_key == key

# ------------------- РЕЄСТРАЦІЯ -------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            return render_template("register.html", error="Заповніть усі поля!")

        with SessionLocal() as db:
            if db.query(User).filter(User.username == username).first():
                return render_template("register.html", error="Користувач вже існує!")

            hashed = create_password_hash(password)
            user = User(username=username, password=hashed)
            db.add(user)
            db.commit()
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("tasks_page"))

    return render_template("register.html")

# ------------------- ЛОГІН -------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_input = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        with SessionLocal() as db:
            user = db.query(User).filter(User.username == username_input).first()
            if user and check_password_hash(password, user.password):
                session["user_id"] = user.id
                session["username"] = user.username
                return redirect(url_for("tasks_page"))
            else:
                return render_template("login.html", error="❌ Невірний логін або пароль!")

    message = request.args.get("message")
    return render_template("login.html", message=message)

# ------------------- ВИХІД -------------------
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("login", message="Ви вийшли з акаунта ✅"))

# ------------------- СТОРІНКА ЗАВДАНЬ -------------------
@app.route("/", methods=["GET"])
def tasks_page():
    if "user_id" not in session:
        return redirect(url_for("login"))

    q = request.args.get("q", "").lower()
    status = request.args.get("status", "")

    with SessionLocal() as db:
        query = db.query(Task).filter(Task.user_id == session["user_id"])
        if q:
            query = query.filter(Task.name.ilike(f"%{q}%"))
        if status:
            query = query.filter(Task.status == status)
        tasks = query.all()

    return render_template("tasks.html", tasks=tasks, search=q, status=status, username=session["username"])

# ------------------- ДОДАВАННЯ ЗАВДАННЯ -------------------
@app.route("/add", methods=["GET", "POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        status = request.form.get("status") or "new"

        if not name:
            return render_template("task_form.html", mode="add",
                                   task={"name": name, "description": description, "status": status},
                                   error="Вкажіть назву завдання!")

        with SessionLocal() as db:
            task = Task(title=name, description=description, status=status, user_id=session["user_id"])
            db.add(task)
            db.commit()

        return redirect(url_for("tasks_page"))

    return render_template("task_form.html", mode="add", task={"name": "", "description": "", "status": "new"})

# ------------------- РЕДАГУВАННЯ ЗАВДАННЯ -------------------
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == session["user_id"]).first()
        if not task:
            return "Завдання не знайдено", 404

        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            description = (request.form.get("description") or "").strip()
            new_status = request.form.get("status") or "new"

            if not title:
                return render_template("task_form.html", mode="edit", task=task, error="Вкажіть назву завдання!")

            task.name = title
            task.description = description
            task.status = new_status
            db.commit()
            return redirect(url_for("tasks_page"))

    return render_template("task_form.html", mode="edit", task=task)

# ------------------- ВИДАЛЕННЯ ЗАВДАННЯ -------------------
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == session["user_id"]).first()
        if task:
            db.delete(task)
            db.commit()

    return redirect(url_for("tasks_page"))

# ------------------- RUN -------------------
if __name__ == "__main__":
    app.run(debug=True)
