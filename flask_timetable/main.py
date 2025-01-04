from flask import Flask, render_template, url_for

from parsinger.parser import GroupsParser

app = Flask(__name__)


@app.route("/")
def navigation():
    return render_template("navigation.html")


@app.route("/new/check")
def chech_new_group(): ...


@app.route("/new/create")
def create_new_group():
    facs =
    courses =
    return render_template("creature.html", faculties=facs, courses=courses)

@app.route("/new/choose", methods=["GET", "POST"])
def choose_group():



@app.route("/teachers")
def teachers(): ...


@app.route("/old", methods=["GET", "POST"])
def get_old_group(): ...


if __name__ == "__main__":
    app.run(debug=True)
