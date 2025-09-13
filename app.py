from flask import Flask, render_template, request, redirect, url_for
from base import create_db, SessionLocal
from models.task import Task

app = Flask(__name__)
create_db()


@app.route("/")
def index():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return render_template("index.html", tasks=tasks)


@app.route("/task_form", methods=["GET", "POST"])
def task_form():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        status = request.form.get("status", "new")

        if not name or not description:
            return "All fields are required"

        db = SessionLocal()
        task = Task(name=name, description=description, status=status)
        db.add(task)
        db.commit()
        db.close()

        return redirect(url_for("index"))

    return render_template("task_form.html", mode="add")


# 📝 Редагування завдання
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    db = SessionLocal()
    task = db.get(Task, task_id)

    if not task:
        db.close()
        return "Task not found", 404

    if request.method == "POST":
        task.name = request.form["name"]
        task.description = request.form["description"]
        task.status = request.form.get("status", task.status)
        db.commit()
        db.close()
        return redirect(url_for("index"))

    db.close()
    return render_template("task_form.html", mode="edit", task=task)


# ❌ Видалення завдання
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    db = SessionLocal()
    task = db.get(Task, task_id)

    if not task:
        db.close()
        return "Task not found", 404

    db.delete(task)
    db.commit()
    db.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)