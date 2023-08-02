import pandas as pd
def Attractions_recommend(recommend):
    Attractions = pd.read_csv('penghu_id.csv',encoding='utf-8-sig')
    Attractions_id = Attractions["id"]
    Attractions_html = Attractions["html"]
    Attractions_imgur = Attractions["imgur"]
    Attractions_map = Attractions["map"]
    for i in range(0,217):
        if Attractions_id[i] == recommend :
            recommend_website = Attractions_html[i]
            recommend_imgur = Attractions_imgur[i]
            recommend_map = Attractions_map[i]
            #print(recommend_website,recommend_imgur,recommend_map)
            break
    
    return recommend_website,recommend_imgur,recommend_map
        
      