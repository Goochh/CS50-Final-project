from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/programs", methods=["GET"])
def programs():
    return render_template("programs.html")

@app.route("/diet", methods=["GET"])
def diet():
    return render_template("diet.html")


@app.route("/statistics", methods=["GET"])
def statistics():
    return render_template("statistics.html")

@app.route("/timer", methods=["GET"])
def timer():
    return render_template("timer.html")

if __name__ == '__main__':
    app.run(debug=True)
