from flask import Flask, render_template, url_for, request
import json

app = Flask(__name__)
PARAMETER = "request"
MAX_NUM = 0


def check_info_file(filename="requests.json"):
    try:
        with open(filename, mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
        with open(filename, mode="x"):
            ...
    except json.JSONDecodeError:
        data = {}

    return data


@app.route("/processing/printer")
def printer():
    data = check_info_file()
    return render_template("table.html", header="All your requests", params=data)


@app.route("/")
def navigation():
    routes = ("printer", "navigation", "processing")
    data = {name: url_for(name) for name in routes}
    return render_template("navigation.html", buttons=data)


@app.route("/processing")
def processing():
    names = ("All requests", "Navigation", "Fill form")
    routes = ("printer", "navigation", "fill_form")
    data = {name: url_for(route) for name, route in zip(names, routes)}
    return render_template("navigation.html", buttons=data, param_name=PARAMETER)


@app.route("/processing/form")
def fill_form():
    data = {"Navigation": url_for("navigation")}
    return render_template("processing.html", buttons=data, param_name=PARAMETER)


@app.route("/processing/req", methods=["POST", "GET"])
def processing_form():
    global MAX_NUM
    if request.method == "POST":
        data = check_info_file()
        data.update({f"{PARAMETER}_{MAX_NUM}": request.form[PARAMETER]})
        MAX_NUM += 1
        with open("requests.json", mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        current_request = request.form
        return render_template(
            "table.html", header="Information", params=current_request
        )


if __name__ == "__main__":
    app.run(debug=True)
