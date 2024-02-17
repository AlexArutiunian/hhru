import json
import os



def create_bunchs(path, full_in):
    with open(full_in, "r", encoding="utf-8") as fp:
        datas = json.load(fp)
    data_bunch = []    
    for i, d in enumerate(datas):
        data_bunch.append(d)
        print(i)
        if i % 1000 == 0:
            print(i)
            with open(path + f"/_{(int)(i/1000)}_2.json", "w", encoding="utf-8") as fp:
                json.dump(data_bunch, fp, ensure_ascii=False, indent=2)
                data_bunch = []

def merge_bunchs(path, full_out):
    data_merged = []  
    for bunch in os.listdir(path):
        with open(path + "/" + bunch, "r", encoding="utf-8") as fp:
            datas = json.load(fp)
          
        for i, d in enumerate(datas):
            data_merged.append(d)
            
    with open(full_out, "w", encoding="utf-8") as fp:
        json.dump(data_merged, fp, ensure_ascii=False, indent=2)
                
            
path = "bunchs"   

merge_bunchs(path, "test.json")      

