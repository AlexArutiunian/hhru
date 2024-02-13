import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

data_fields = pd.read_csv("fields.csv")
data_spec = pd.read_csv("spec.csv")
ua = UserAgent()

all_vacancy = []

async def fetch_vacancies(session, id_field, id_spec, industry, prof_role):
    url = f"https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&industry={id_field}&professional_role={id_spec}"

    async with session.get(url) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "html.parser")

        items_vacancy = soup.find_all("span", class_="serp-item__title-link-wrapper")
        for item in items_vacancy:
            data_links_vacancy = {
                "vacancy_name": item.get_text(),
                "link": item.find("a").get("href"),
                "industry": industry,
                "professional_role": prof_role,
                "link_list_vacancy_where_it_is": url,
                "id_pair": (id_field, id_spec)
            }
            all_vacancy.append(data_links_vacancy)

async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for index, row in data_fields.iterrows():
            
            id_field = row["id"]
            industry = row["name_field"]
            for index2, row2 in data_spec.iterrows():
                
                print(index, len(data_spec.iterrows()))
            
                prof_role = row2["name_spec"]
                id_spec = row2["id"]
                print(id_field, id_spec)
                print(industry, prof_role)
                await fetch_vacancies(session, id_field, id_spec, industry, prof_role)

    with open("vacancy_links.json", "w", encoding="utf-8") as fp:
        json.dump(all_vacancy, fp, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    asyncio.run(main())