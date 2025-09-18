import hashlib
import os

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_secret_key_that_is_long_and_random"

tasks = [
    {"id": 1, "title": "Купити продукти", "description": "Молоко, хліб, яйця", "status": "new"},
    {"id": 2, "title": "Написати звіт", "description": "По проекту Flask", "status": "in_progress"},
    {"id": 3, "title": "Зробити домашку", "description": "Алгебра та геометрія", "status": "done"},
]

users = {}


def create_password_hash(password):
    """Генерує випадкову сіль, хешує пароль разом з нею та повертає сіль і хеш."""
    salt = os.urandom(32)  # 32 байти випадкової солі
    key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )
    return salt.hex(), key.hex()


def check_password_hash(password, stored_salt_hex, stored_hash_hex):
    """Перевіряє пароль, використовуючи збережену сіль та хеш."""
    salt = bytes.fromhex(stored_salt_hex)
    stored_hash = bytes.fromhex(stored_hash_hex)
    key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )
    return key == stored_hash


def next_id():
    """Визначає наступний доступний ID для завдання."""
    return (max([t["id"] for t in tasks]) + 1) if tasks else 1


@app.route("/register", methods=["GET", "POST"])
def register():
    """Реєстрація нового користувача."""
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            return render_template("auth.html", mode="register", error="Заповніть усі поля!")

        if username in users:
            return render_template("auth.html", mode="register", error="Користувач вже існує!")

        salt, hashed_password = create_password_hash(password)
        users[username] = {"salt": salt, "hash": hashed_password}
        session["username"] = username
        return redirect(url_for("tasks_page"))

    return render_template("auth.html", mode="register")


@app.route("/register", methods=["GET", "POST"])
def login():
    """Вхід існуючого користувача."""
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if username in users and check_password_hash(
            password, users[username]["salt"], users[username]["hash"]
        ):
            session["username"] = username
            return redirect(url_for("tasks_page"))
        else:
            return render_template("auth.html", mode="login", error="❌ Невірний логін або пароль!")

    return render_template("auth.html", mode="login")


@app.route("/register")
def logout():
    """Вихід з облікового запису."""
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/", methods=["GET"])
def tasks_page():
    """Головна сторінка зі списком завдань."""
    if "username" not in session:
        return redirect(url_for("login"))

    q = request.args.get("q", "").lower()
    status = request.args.get("status", "")

    filtered = tasks
    if q:
        filtered = [t for t in filtered if q in t["title"].lower()]
    if status:
        filtered = [t for t in filtered if t["status"] == status]

    return render_template("tasks.html", tasks=filtered, search=q, status=status, username=session["username"])


@app.route("/add", methods=["GET", "POST"])
def add_task():
    """Додавання нового завдання."""
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        status = request.form.get("status") or "new"

        if not title:
            return render_template(
                "task_form.html",
                mode="add",
                error="Вкажіть назву завдання!",
                task={"title": title, "description": description, "status": status},
            )

        new_task = {
            "id": next_id(),
            "title": title,
            "description": description,
            "status": status,
        }
        tasks.append(new_task)

        empty = {"title": "", "description": "", "status": "new"}
        return render_template("task_form.html", mode="add", task=empty, success="✅ Завдання додано!")

    empty = {"title": "", "description": "", "status": "new"}
    return render_template("task_form.html", mode="add", task=empty)


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """Редагування існуючого завдання."""
    if "username" not in session:
        return redirect(url_for("login"))

    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return "Завдання не знайдено", 404

    q = request.args.get("q")
    status_filter = request.args.get("status")

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        new_status = request.form.get("status") or "new"

        if not title:
            return render_template(
                "task_form.html",
                mode="edit",
                error="Вкажіть назву завдання!",
                task={"title": title, "description": description, "status": new_status},
                task_id=task_id,
            )

        task["title"] = title
        task["description"] = description
        task["status"] = new_status

        return redirect(url_for("tasks_page", q=q, status=status_filter))

    return render_template("task_form.html", mode="edit", task=task, task_id=task_id)


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Видалення завдання."""
    if "username" not in session:
        return redirect(url_for("login"))

    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]

    q = request.args.get("q")
    status_filter = request.args.get("status")
    return redirect(url_for("tasks_page", q=q, status=status_filter))


if __name__ == "__main__":
    app.run(debug=True)

