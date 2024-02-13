import json

path = "vacancy_links.json"

with open(path, "r", encoding="utf-8") as fp:
    data = json.load(fp)

print(len(data))    