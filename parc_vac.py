import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from icecream import ic
import json



def parc_vac(url):
    
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }
    
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    
    name_vacancy = soup.find("h1", class_="bloko-header-section-1")
    salary = soup.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite")
    experience = soup.find("p", class_="vacancy-description-list-item")
    name_company = soup.find_all("span", class_="bloko-header-section-2 bloko-header-section-2_lite")[1]
    desc = soup.find("div", class_="vacancy-description")
    time_creation = soup.find("p", class_="vacancy-creation-time-redesigned")
    skills_divs = soup.find_all("div", class_="bloko-tag bloko-tag_inline")
    
    skills = []
    
    for item in skills_divs:
        skills.append(item.get_text().replace("\xa0", " "))
    
    data = {
        "name_vacancy": name_vacancy.get_text(),
        "salary": salary.get_text().replace("\xa0", " "),
        "experience": experience.get_text(),
        "name_company": name_company.get_text().replace("\xa0", " "),
        "description": desc.get_text().replace("О компании", ""),
        "time_creation": time_creation.get_text().replace("\xa0", " "),
        "skills": skills  
    }
    
    ic(data)
    
    return data

path = "vacancy_links2.json"
path_out = "2ndpart.json"
with open(path, "r", encoding="utf-8") as fp:
    datas = json.load(fp)

datas_out = []

for data in datas:
    try:
        result = {**data, **parc_vac(data["link"])}
        datas_out.append(result)  
        
        with open(path_out, "w", encoding="utf-8") as fp:
            json.dump(datas_out, fp, ensure_ascii=False, indent=2)
    except Exception as e:
        with open("err.txt", "a", encoding="utf-8") as fp:
            fp.write(" field " + (str)(data["id_pair"][0]))  
            fp.write(" spec " + (str)(data["id_pair"][1])) 
            fp.write(" vac name " + (str)(data["link"]))  
            fp.write(" vac name " + (str)(data["vacancy_name"]) + "\n")     
