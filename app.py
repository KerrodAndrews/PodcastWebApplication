from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def show_layout():
    return render_template('layout.html')


if __name__ == '__app__':
    app.run(debug=True, port=5000)
