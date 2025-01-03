from flask import Flask

from parsinger.parser import GroupsParser

app = Flask(__name__)


@app.route("/")
def navigation(): ...


@app.route("/new")
def create_new_group(): ...


@app.route("/teachers")
def teachers(): ...


@app.route("/old")
def get_old_group(): ...


if __name__ == "__main__":
    app.run(debug=True)
