from flask import Flask, render_template, url_for, request, render_template_string


from parsinger.parser import GroupsParser
from parsinger.preparations import Preparations
from parsinger.managers import Manager
from parsinger.times import Clocks
from flask_timetable.settings import FILE
from handlers.handle import CreatorTimetables

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
        value = periods[clocks.define_need_period(periods.keys(), clocks.today)]
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
        group_name, group_url = request.form["group"].split(", ")
        print(group_name, group_url)
        data = manager.get_from(FILE)
        data.update({"group": group_name})
        manager.save_to(data, FILE)
        parser.create_config(group_url)
        return render_template("your_group.html", group_name=group_name)

    if request.method == "GET":
        try:
            data = manager.get_from(FILE)
            group_name = data.get("group")
        except FileNotFoundError:
            group_name = None
        return render_template("your_group.html", group_name=group_name)


@app.route("/timetable/today")
def get_today():
    timetable = parser.get_timetable("today")
    html_creator = CreatorTimetables(timetable)
    date, body = html_creator.create_today()
    html = html_creator.convert_into_text(bs_object=body)
    return render_template("timetable_template.html", html_text=html)


@app.route("/timetable/tomorrow")
def get_tomorrow():
    timetable = parser.get_timetable("tomorrow")
    html_creator = CreatorTimetables(timetable)
    date, body = html_creator.create_tomorrow()
    html = html_creator.convert_into_text(bs_object=body)
    return render_template("timetable_template.html", html_text=html)


@app.route("/timetable/this_week")
def get_this_week():
    timetable = parser.get_timetable("this_week")
    html_creator = CreatorTimetables(timetable)
    html = html_creator.create_week()
    return render_template("timetable_template.html", html_text=html)


@app.route("/timetable/next_week")
def get_next_week():
    timetable = parser.get_timetable("next_week")
    html_creator = CreatorTimetables(timetable)
    html = html_creator.create_week()
    return render_template("timetable_template.html", html_text=html)


if __name__ == "__main__":
    manager = Manager()
    config = Preparations()
    parser = GroupsParser(config)
    clocks = Clocks()
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True)
