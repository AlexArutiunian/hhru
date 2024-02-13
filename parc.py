import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from icecream import ic
import json

data_fields = pd.read_csv("fields.csv")
data_spec = pd.read_csv("spec.csv")
ua = UserAgent()

all_vacancy = []

for index, row in data_fields.iterrows():
    id_field = row["id"]
    for index2, row2 in data_spec.iterrows():
        industry = row["name_field"]
        prof_role = row2["name_spec"]
        id_spec = row2["id"]

        
        headers = {
            "User-Agent": ua.random
        }

        print(id_field, id_spec)
        
        
        
        for i_page in range(1, 30):
            url = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&industry={id_field}&professional_role={id_spec}"
            req = requests.get(url, headers=headers)

            soup = BeautifulSoup(req.text, "html.parser")

            items_vacancy = soup.find_all("span", class_="serp-item__title-link-wrapper")
            url += f"&page{i_page}"
            for item in items_vacancy:
                data_links_vacancy = {
                    "vacancy_name" : item.get_text(),
                    "link": item.find("a").get("href"),
                    "industry": industry,
                    "professional_role": prof_role,
                    "link_list_vacancy_where_it_is": url,
                    "id_pare": (id_field, id_spec)
                }  
               # ic(data_links_vacancy)  
                all_vacancy.append(data_links_vacancy)
            with open("vacancy_links.json", "w", encoding="utf-8") as fp:
                json.dump(all_vacancy, fp, ensure_ascii=False, indent=4)

    #   print(id_field, id_spec)

    #   print(url)