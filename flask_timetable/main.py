from flask import (
    Flask,
    render_template,
    url_for,
    request,
    render_template_string,
    flash,
    session,
    redirect,
)
import uuid
import datetime

from parsinger.parser import GroupsParser, TeacherParser
from parsinger.preparations import Preparations
from parsinger.managers import Manager
from parsinger.times import Clocks
from flask_timetable.settings import FILE, FILE_T
from handlers.handle import CreatorTimetables


app = Flask(__name__)
app.config["SECRET_KEY"] = uuid.uuid4().hex


@app.errorhandler(404)
def not_found(error):
    return (render_template("not_found.html", title="Not Found"), 404)


@app.route("/map")
def get_map():
    return render_template("ya_map.html", title="Ya_map")


@app.route("/")
def get_navigation_page():
    return render_template("navigation.html", title="Navigation_page")


@app.route("/profile")
def profile():
    if "user" in session:
        return render_template(
            "profile.html", title="Profile_page", user=session["user"]
        )
    # else:
    #     return отдельно для того чтобы зарегатьься


@app.route("/authorisation", methods=["GET", "POST"])
def authorisation():
    if "user" in session:
        return redirect(url_for("profile"))
    if request.method == "GET":
        username = None

    if request.method == "POST":
        if request.form["passwd"] == "1234":
            session["user"] = request.form["user"]
            return redirect(url_for("profile"))
        else:
            flash(message="Введен неверный пароль", category="is-invalid")
            username = request.form["user"]

    return render_template(
        "authorisation.html", title="Authorisation_page", username=username
    )


@app.route("/authorisation/sign_up")  # ну и тут нужно прикрутить redirect
def sign_up():
    if request.method == "POST":
        ...


@app.route("/authorisation/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("get_navigation_page"))


@app.route("/new/check")
def chech_new_group(): ...


@app.route("/new/create", methods=["GET", "POST"])
def create_new_group():
    pers, fac, cors = group_parser.parameter_names
    if request.method == "GET":
        facs = group_parser.get_parameter_values(fac)
        courses = group_parser.get_parameter_values(cors)
        print(facs, {cors: courses})
        return render_template(
            "creature.html",
            faculties=facs,
            courses=courses,
            fac=fac,
            cor=cors,
            title="Create_group",
        )

    if request.method == "POST":
        params = dict(request.form)
        periods = group_parser.get_parameter_values(pers)
        value = periods[clocks.define_need_period(periods.keys(), clocks.today)]
        params.update({pers: value})

        manager.save_to(params, FILE)
        groups = group_parser.get_groups()
        return render_template(
            "create_groups.html", groups=groups, group="group", title="Create_group"
        )


@app.route("/new/choose", methods=["GET", "POST"])
def choose_group(): ...


@app.route("/old", methods=["GET", "POST"])
def get_old_group():
    if request.method == "POST":
        group_name, group_url = request.form["group"].split(", ")
        print(group_name, group_url)
        data = manager.get_from(FILE)
        data.update({"group": group_name})
        manager.save_to(data, FILE)
        group_parser.create_config(group_url)

    if request.method == "GET":
        data = manager.get_from(FILE)
        if data is None:
            group_name = None
        else:
            group_name = data.get("group", None)

    return render_template("your_group.html", group_name=group_name, title="Your_group")


@app.route("/group/timetable/today")
def get_today():
    timetable = group_parser.get_timetable("today")
    html_creator = CreatorTimetables(timetable)
    date, body = html_creator.create_today()
    html = html_creator.convert_into_text(bs_object=body)
    return render_template("timetable_template.html", html_text=html, title="Timetable")


@app.route("/group/timetable/tomorrow")
def get_tomorrow():
    timetable = group_parser.get_timetable("tomorrow")
    html_creator = CreatorTimetables(timetable)
    date, body = html_creator.create_tomorrow()
    html = html_creator.convert_into_text(bs_object=body)
    return render_template("timetable_template.html", html_text=html, title="Timetable")


@app.route("/group/timetable/this_week")
def get_this_week():
    timetable = group_parser.get_timetable("this_week")
    html_creator = CreatorTimetables(timetable)
    html = html_creator.create_week()
    return render_template("timetable_template.html", html_text=html, title="Timetable")


@app.route("/group/timetable/next_week")
def get_next_week():
    timetable = group_parser.get_timetable("next_week")
    html_creator = CreatorTimetables(timetable)
    html = html_creator.create_week()
    return render_template("timetable_template.html", html_text=html, title="Timetable")


@app.route("/teachers", methods=["GET", "POST"])
def get_teachers():
    if request.method == "POST":
        teacher_name, teacher_url = request.form["teacher"].split(", ")
        print(teacher_name, teacher_url)
        data = manager.get_from(FILE_T)
        data.update({"teacher": teacher_name})
        manager.save_to(data, FILE_T)
        teacher_parser.create_config(teacher_url)

    if request.method == "GET":
        data = manager.get_from(FILE_T)
        if data is None:
            teacher_name = None
        else:
            teacher_name = data.get("teacher")

    return render_template("teachers.html", teacher=teacher_name, title="Teacher")


@app.route("/teachers/create", methods=["GET", "POST"])
def create_teachers():
    pers, sstring = teacher_parser.parameter_names
    if request.method == "GET":
        return render_template(
            "create_teacher.html", sstring=sstring, title="Create_teacher"
        )

    if request.method == "POST":
        params = dict(request.form)
        periods = teacher_parser.get_parameter_values(pers)
        value = periods[clocks.define_need_period(periods.keys(), clocks.today)]
        params.update({pers: value})

        manager.save_to(params, FILE_T)
        teachers = teacher_parser.get_teachers()
        if teachers == {}:
            teachers = None
        return render_template(
            "select_teacher.html",
            sstring=sstring,
            teachers=teachers,
            teacher="teacher",
            title="Create_teacher",
            text=params["sstring"],
        )


@app.route("/teachers/timetable/today")
def get_teacher_today():
    timetable = teacher_parser.get_timetable("today")
    html_creator = CreatorTimetables(timetable)
    date, body = html_creator.create_today()
    html = html_creator.convert_into_text(bs_object=body)
    return render_template("timetable_template.html", html_text=html, title="Timetable")


@app.route("/teachers/timetable/tomorrow")
def get_teacher_tomorrow():
    timetable = teacher_parser.get_timetable("tomorrow")
    html_creator = CreatorTimetables(timetable)
    date, body = html_creator.create_tomorrow()
    html = html_creator.convert_into_text(bs_object=body)
    return render_template("timetable_template.html", html_text=html, title="Timetable")


@app.route("/teachers/timetable/this_week")
def get_teacher_this_week():
    timetable = teacher_parser.get_timetable("this_week")
    html_creator = CreatorTimetables(timetable)
    html = html_creator.create_week()
    return render_template("timetable_template.html", html_text=html, title="Timetable")


@app.route("/teachers/timetable/next_week")
def get_teacher_next_week():
    timetable = teacher_parser.get_timetable("next_week")
    html_creator = CreatorTimetables(timetable)
    html = html_creator.create_week()
    return render_template("timetable_template.html", html_text=html, title="Timetable")


if __name__ == "__main__":
    manager = Manager()
    config = Preparations()
    group_parser = GroupsParser(config)
    teacher_parser = TeacherParser(config)
    clocks = Clocks()
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True)
