from flask import Flask, render_template, url_for, request

from parsinger.parser import GroupsParser
from parsinger.preparations import Preparations
from parsinger.managers import Manager

app = Flask(__name__)


@app.route("/")
def navigation():
    return render_template("navigation.html")


@app.route("/new/check")
def chech_new_group(): ...


@app.route("/new/create", methods=["GET", "POST"])
def create_new_group():
    if request.method == "GET":
        facs = parser.get_parameter_values("facs")
        courses = parser.get_parameter_values("courses")
        print(facs, courses)
        return render_template("creature.html", faculties=facs, courses=courses)
    if request.method == "POST":
        manager = Manager()
        params = request.form
        manager.save_to(params, "group_selection.json")


@app.route("/new/choose", methods=["GET", "POST"])
def choose_group(): ...


@app.route("/teachers")
def teachers(): ...


@app.route("/old", methods=["GET", "POST"])
def get_old_group(): ...


if __name__ == "__main__":
    config = Preparations()
    parser = GroupsParser(config)
    app.run(debug=True)
