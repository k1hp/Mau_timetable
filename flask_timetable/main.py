from flask import Flask, render_template, url_for, request

from parsinger.parser import GroupsParser
from parsinger.preparations import Preparations
from parsinger.managers import Manager
from parsinger.times import Clocks

app = Flask(__name__)


@app.route("/")
def navigation():
    return render_template("navigation.html")


@app.route("/new/check")
def chech_new_group(): ...


@app.route("/new/create", methods=["GET", "POST"])
def create_new_group():
    pers, fac, cors = parser.parameter_names
    if request.method == "GET":
        facs = parser.get_parameter_values(fac)
        courses = parser.get_parameter_values(cors)
        print(facs, {cors: courses})
        return render_template(
            "creature.html", faculties=facs, courses=courses, fac=fac, cor=cors
        )

    if request.method == "POST":
        params = dict(request.form)
        periods = parser.get_parameter_values(pers)
        value = periods[clocks.define_today_period(periods.keys())]
        params.update({pers: value})

        manager.save_to(params, FILE)
        groups = parser.get_groups()
        return render_template("create_groups.html", groups=groups, group="group")


@app.route("/new/choose", methods=["GET", "POST"])
def choose_group(): ...


@app.route("/teachers")
def teachers(): ...


@app.route("/old", methods=["GET", "POST"])
def get_old_group():
    if request.method == "POST":
        group_name = request.form["group"]
        data = manager.get_from(FILE)
        data.update({"group": group_name})
        manager.save_to(data, FILE)
        return render_template("your_group.html", group_name=group_name)

    if request.method == "GET":
        try:
            data = manager.get_from(FILE)
            group_name = data.get("group")
        except FileNotFoundError:
            group_name = None
        return render_template("your_group.html", group_name=group_name)


if __name__ == "__main__":
    manager = Manager()
    config = Preparations()
    parser = GroupsParser(config)
    clocks = Clocks()
    FILE = "group_selection.json"
    app.run(host="0.0.0.0", port=5000, debug=True)
