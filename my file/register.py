from flask import Flask

app = Flask(__name__)

@app.route("/")
def register():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Регистрация</title>
    </head>
    <body>
        <h2>Форма регистрации</h2>
        <form method="post" action="/register">
            <label>Имя: <input type="text" name="username"></label><br><br>
            <label>Email: <input type="email" name="email"></label><br><br>
            <label>Пароль: <input type="password" name="password"></label><br><br>
            <button type="submit">Зарегистрироваться</button>
        </form>
        <a href="http://127.0.0.1:5000/">Вход</a> |
        <a href="http://127.0.0.1:5002/">Выход</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(port=5001, debug=True)
