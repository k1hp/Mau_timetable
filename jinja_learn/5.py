import json

banger = {"lst": [10, 23]}

with open("requests.json", mode="a+", encoding="utf-8") as file:
    try:
        data = json.load(file)
    except Exception:
        data = {}
    # if data is None:
    #     data.update(banger)
    # json.dump(data, file, indent=4)
print(data, data.__class__)
