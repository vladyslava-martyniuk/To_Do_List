from flask import Flask

app = Flask(__name__)

@app.route("/")
def logout():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Выход</title>
    </head>
    <body>
        <h2>Вы успешно вышли из системы!</h2>
        <a href="http://127.0.0.1:5000/">Войти</a> |
        <a href="http://127.0.0.1:5001/">Регистрация</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(port=5002, debug=True)
