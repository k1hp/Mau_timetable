from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/printer")
def printer():
    return "Это принтер"


@app.route("/")
def navigation():
    routes = ("printer", "navigation", "processing")
    data = {name: url_for(name) for name in routes}
    return render_template("navigation.html", buttons=data)


@app.route("/processing/<user>/<password>")
@app.route("/processing")
def processing(user, password):
    params = {"user": user, "password": password}
    return render_template("table.html", params=params)


if __name__ == "__main__":
    app.run(debug=True)
