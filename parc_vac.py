import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from icecream import ic
import json
import time


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
    try:
        name_company = (soup.find_all("span", class_="bloko-header-section-2 bloko-header-section-2_lite")[1]).get_text().replace("\xa0", " ")
    except:
        name_company = ""    
    try:
        desc = soup.find("div", class_="vacancy-description").get_text().replace("О компании", "")
    except:
        desc = ""
    try:        
        time_creation = soup.find("p", class_="vacancy-creation-time-redesigned").get_text().replace("\xa0", " ")
    except: 
        time_creation = ""  
          
    skills_divs = soup.find_all("div", class_="bloko-tag bloko-tag_inline")
    
    skills = []
    
    for item in skills_divs:
        skills.append(item.get_text().replace("\xa0", " "))
    
    data = {
        "name_vacancy": name_vacancy.get_text(),
        "salary": salary.get_text().replace("\xa0", " "),
        "experience": experience.get_text(),
        "name_company": name_company,
        "description": desc,
        "time_creation": time_creation,
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
    time.sleep(3)
    try:
        result = {**data, **parc_vac(data["link"])}
        datas_out.append(result)  
        
        with open(path_out, "w", encoding="utf-8") as fp:
            json.dump(datas_out, fp, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e, data["link"])
        continue        
