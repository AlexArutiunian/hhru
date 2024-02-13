import json
from bs4 import BeautifulSoup
import re
from icecream import ic
import pandas as pd

def remove_digits(input_string):
    return ''.join([char for char in input_string if not char.isdigit()])

def remove_non_digits(input_string):
    return ''.join([char for char in input_string if char.isnumeric()])

type_ = "spec"

path = f"ITEMS_{type_}.html"

with open(path, "r", encoding="utf-8") as fp:
    html = fp.read()

soup = BeautifulSoup(html, "html.parser")

fields_divs = soup.find_all("div", class_="bloko-tree-selector-item bloko-tree-selector-item_no-children")
data_list = []
print(fields_divs[0])
for d in fields_divs:
    span = d.get("data-qa")
    print(span)
    num = remove_non_digits(span)
    name_field = remove_digits(d.get_text()).replace("\xa0\u202f", "")
    data_list.append({'id': num, f'name_{type_}': name_field})

ic(data_list)
print(len(data_list))

df = pd.DataFrame(data_list)

# Запись в Excel
excel_path = f"{type_}.xlsx"
df.to_excel(excel_path, index=False)  # index=False чтобы не сохранять индексы

# Запись в CSV
csv_path = f"{type_}.csv"
df.to_csv(csv_path, index=False) 
df.to_excel(f"{type_}.xlsx")

    