from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)


tasks = [
    {"id": 1, "title": "Купити продукти", "description": "Молоко, хліб, яйця", "status": "new", "due_date": "2025-09-20"},
    {"id": 2, "title": "Написати звіт", "description": "По проекту Flask", "status": "in_progress", "due_date": "2025-09-19"},
    {"id": 3, "title": "Зробити домашку", "description": "Алгебра та геометрія", "status": "done", "due_date": "2025-09-15"},
]

def next_id():
    return (max([t["id"] for t in tasks]) + 1) if tasks else 1

@app.route("/", methods=["GET"])
def tasks_page():
    q = request.args.get("q", "").lower()
    status = request.args.get("status", "")
    date_filter = request.args.get("date", "")

    filtered = tasks
    if q:
        filtered = [t for t in filtered if q in t["title"].lower()]
    if status:
        filtered = [t for t in filtered if t["status"] == status]
    if date_filter:
        filtered = [t for t in filtered if t["due_date"] == date_filter]

    return render_template(
        "tasks.html",
        tasks=filtered, search=q, status=status, date=date_filter
    )

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        form = request.form
        title = (form.get("title") or "").strip()
        if not title:
            return render_template("task_form.html", mode="add", error="Вкажіть назву завдання!", task=form)

        new_task = {
            "id": next_id(),
            "title": title,
            "description": (form.get("description") or "").strip(),
            "status": form.get("status") or "new",
            "due_date": form.get("due_date") or date.today().isoformat(),
        }
        tasks.append(new_task)
        return redirect(url_for("tasks_page"))

    empty = {"title": "", "description": "", "status": "new", "due_date": date.today().isoformat()}
    return render_template("task_form.html", mode="add", task=empty)

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return "Завдання не знайдено", 404

    if request.method == "POST":
        form = request.form
        title = (form.get("title") or "").strip()
        if not title:
            return render_template("task_form.html", mode="edit", error="Вкажіть назву завдання!", task=form, task_id=task_id)

        task["title"] = title
        task["description"] = (form.get("description") or "").strip()
        task["status"] = form.get("status") or "new"
        task["due_date"] = form.get("due_date") or task.get("due_date")
        return redirect(url_for("tasks_page"))

    return render_template("task_form.html", mode="edit", task=task, task_id=task_id)

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("tasks_page"))

if __name__ == "__main__":
    app.run(debug=True)
