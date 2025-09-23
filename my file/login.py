from flask import Flask

app = Flask(__name__)

@app.route("/")
def login():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Вход</title>
    </head>
    <body>
        <h2>Форма входа</h2>
        <form method="post" action="/login">
            <label>Логин: <input type="text" name="username"></label><br><br>
            <label>Пароль: <input type="password" name="password"></label><br><br>
            <button type="submit">Войти</button>
        </form>
        <a href="http://127.0.0.1:5001/">Регистрация</a> |
        <a href="http://127.0.0.1:5002/">Выход</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(port=5000, debug=True)
