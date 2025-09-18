from flask import Flask, render_template, request, redirect, url_for, session
import hashlib

app = Flask(__name__)
app.secret_key = "super_secret_key"  

tasks = [
    {"id": 1, "title": "Купити продукти", "description": "Молоко, хліб, яйця", "status": "new"},
    {"id": 2, "title": "Написати звіт", "description": "По проекту Flask", "status": "in_progress"},
    {"id": 3, "title": "Зробити домашку", "description": "Алгебра та геометрія", "status": "done"},
]

users = {}  


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def next_id():
    return (max([t["id"] for t in tasks]) + 1) if tasks else 1



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            return render_template("auth.html", mode="register", error="Заповніть усі поля!")

        if username in users:
            return render_template("auth.html", mode="register", error="Користувач вже існує!")

        users[username] = hash_password(password)
        session["username"] = username
        return redirect(url_for("tasks_page"))

    return render_template("auth.html", mode="register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if username in users and users[username] == hash_password(password):
            session["username"] = username
            return redirect(url_for("tasks_page"))
        else:
            return render_template("auth.html", mode="login", error="❌ Невірний логін або пароль!")

    return render_template("auth.html", mode="login")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))



@app.route("/", methods=["GET"])
def tasks_page():
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
    if "username" not in session:
        return redirect(url_for("login"))

    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]

    q = request.args.get("q")
    status_filter = request.args.get("status")
    return redirect(url_for("tasks_page", q=q, status=status_filter))


if __name__ == "__main__":
    app.run(debug=True)
