import googlemaps
from time import sleep 

import configparser
def googlemap_search(lng,lat):
    #get api key
   
    gmaps=googlemaps.Client(key="AIzaSyA2sdW7WdzWaqGpxVq3zt3F4LC-RWTCmHQ")
    #change to dictionary
    loc={'lat':lat,'lng':lng}
    #搜尋2km裡的民宿
    rad=2000
    search_number=len(gmaps.places_nearby(keyword="住宿",radius=rad,location=loc)['results'])
    
    placeID_list=[]
    for place in gmaps.places_nearby(keyword="住宿",radius=rad,location=loc)['results']:
        placeID_list.append(place['place_id'])

    hotel_info=[]
    for id in placeID_list:
        hotel_info.append(gmaps.place(place_id=id,language="zh-TW")['result'])
        sleep(0.1)
        
    name_list=[]
    loc_list=[]
    latitude_list=[]
    longtitude_list=[]
    for h in hotel_info:
        #print(h['name'])
        #print(h['geometry']['location'])
        if len(h['name'])>=50:          #如果民宿名稱的字數大於50，把40項之後的刪除
            h['name']=list(h['name'])
            del h['name'][40:len(h['name'])-1]
            h['name']=''.join(h['name'])
        name_list.append(h['name'])
        latitude_list.append(h['geometry']['location']['lat'])
        longtitude_list.append(h['geometry']['location']['lng'])
        #print("結束1")
        #print("name_list=",name_list,"loc_list=",loc_list)
    #print("結束2")
    #print("共找到",search_number,"筆資料")
    #print("類型",type(hotel_info))
    return name_list,latitude_list,longtitude_list
#search_name,name_list,loc_list=googlemap_search(121.1952988,24.9681558,"餐廳")

def googlemap_search_nearby(lng,lat,keyword):
    #get api key
    api_key = "AIzaSyA2sdW7WdzWaqGpxVq3zt3F4LC-RWTCmHQ"
   
    gmaps=googlemaps.Client(key="AIzaSyA2sdW7WdzWaqGpxVq3zt3F4LC-RWTCmHQ")
    #change to dictionary
    loc={'lat':lat,'lng':lng}
    #搜尋2km裡的民宿
    rad=2000
    search_number=len(gmaps.places_nearby(keyword=keyword,radius=rad,location=loc)['results'])
    
    placeID_list=[]
    for place in gmaps.places_nearby(keyword=keyword,radius=rad,location=loc)['results']:
        placeID_list.append(place['place_id'])
    
    hotel_info=[]
    for id in placeID_list:
        hotel_info.append(gmaps.place(place_id=id,language="zh-TW")['result'])
        sleep(0.1)
    
        
    search_list=[]
    
    maxwidth=800
    
    for h in hotel_info:
        #print("check")

        try:
            photoreference=h['photos'][0]['photo_reference']
            url=f'https://maps.googleapis.com/maps/api/place/photo?maxwidth={maxwidth}&photoreference={photoreference}&key={api_key}'
        except Exception:
            url="no information"
        try:
            price_level=h['price_level']
        except Exception:
            price_level="N/A"
        try:
            rating=h['rating']
        except Exception:
            rating="N/A"
        
        dic={'name':h['name'],
             'price_level':price_level,
             'rating':rating,
             'url':url,
             'place_id':h["place_id"],
             'location':h['geometry']['location']}
        search_list.append(dic)
    return search_list,search_number
#search_list=googlemap_search_nearby(121.1952988,24.9681558,"餐廳")
#print(search_list)

print(googlemap_search(119.57694,23.5729))
#print(googlemap_search_nearby(121.1952988,24.9681558,"學校"))