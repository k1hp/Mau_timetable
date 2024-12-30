from jinja2 import Template, Environment, FileSystemLoader

loader = FileSystemLoader(r"C:\Users\USER\PycharmProjects\Mau_timetable\parsinger")
env = Environment(loader=loader)
template = env.get_template("timetable.html")

msg = template.render()

with open("jinja_!.html", "w", encoding="utf-8") as f:
    print(msg, file=f)
