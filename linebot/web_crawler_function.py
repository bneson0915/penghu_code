import requests
from bs4 import BeautifulSoup
import time
def classify(number):
    #把string 轉成小數再輸出int
    number=round(float(number))
    if number<=3:
        return 0
    elif number>3 and number<=10:
        return 1
    elif  number>10 and number<=25:
        return 2
    else:
        return 3
def search_rain():
    localtime=time.localtime()
    
    year=time.strftime("%Y",localtime)
    month=time.strftime("%m",localtime)
    date=time.strftime("%d",localtime)
    
    response=requests.get(f'https://www.tianqi24.com/penghu/history{year}{month}.html')
    soup=BeautifulSoup(response.text,"html.parser")
    
    grandparent=soup.find('ul',class_="col6")
    #print(grandparent.prettify())
    parent=grandparent.find('li')
    #第一個搜尋的是總覽
    parent=parent.find_next_sibling('li')
    while(1):
        target=parent.find('div')
        #第一欄是日期
        website_date=target.get_text().split('-')
        #print("result= ",website_date[1])
        if (website_date[1]==date):
            #往後五次
            for j in range(0,6):
                target=target.find_next_sibling('div')
            #大問題  df.at[i,'weather']為np.float (解決方法:將excel裡的數值先全部拉0)
            result=classify(target.get_text())
            # print(type(result))
            break
        else:
            parent=parent.find_next_sibling('li')
    return result
print(search_rain())