import csv
import pandas as pd
def crowd(file,time):
    # 打開 CSV 檔案
    with open(file, mode='r', newline='' , encoding='utf-8-sig') as rfile:
        # 設置 CSV 讀取器
        reader = csv.DictReader(rfile)
        # 設置篩選條件
        filter_condition = {'UserID/MemID': userID}
        fieldnames = ['no','Time','POI','UserID/MemID','設置點','緯度','經度','BPL UID','age','gender','天氣']
        with open('C:/Users/roy88/testproject/python/PH/now_crowd.csv', mode='w', newline='' , encoding='utf-8-sig') as wfile:
            # 設置 CSV 寫入器
            writer = csv.DictWriter(wfile ,fieldnames=fieldnames)
            # 寫入欄位名稱
            #writer.writeheader()
            # 逐行讀取 CSV 檔案
            for row in reader:
                # 檢查是否符合篩選條件
                if all(row[key] == value for key, value in filter_condition.items()):
                    # 符合篩選條件，進行操作
                    writer.writerow(row)
                    #print(type(row))

filter('C:/Users/roy88/testproject/python/PH/Beacon20220907-crowd.csv','13') 