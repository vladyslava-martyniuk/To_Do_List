from flask import Flask, render_template
from base import create_db, drop_db

from models.user import User
from models.task import Task

app = Flask("__name__")


create_db()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)