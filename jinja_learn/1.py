from jinja2 import Template, Environment, FileSystemLoader

data = {"1": "БИВТ-ВП-23", "2": "БИВТ-ВТД-23", "3": "АТПП-22"}

loader = FileSystemLoader("")
env = Environment(loader=loader)
template = env.get_template("jinja_test.html")

msg = template.render(data=data)

with open("jinja_!.html", "w", encoding="utf-8") as f:
    print(msg, file=f)
