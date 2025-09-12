from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/task_form', methods=['GET', 'POST'])
def task_form():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('task_form.html')
if __name__ == '__main__':
    app.run(debug=True)