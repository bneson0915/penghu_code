from flask import Flask, request
from gevent.pywsgi import WSGIServer
from random import randrange
import numpy as np
import googlemap_function
import ML
import Search
import Now_weather

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
#from linebot.models import MessageEvent, TextMessage, TextSendMessage 
from linebot.models import *

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = '9L8HgvDkVZgSZZy6S9ihK2r/6UJv5miDFNjHJt0FKfs4yITvDESQAKhiKAyLIAWK8Kjn55api/1/25vC8aceJUhjr23DfqJsxkIJuYH6v7gHjRRzRSHssanGqt873C6i8rp9BxmT4BsrMILekVSppwdB04t89/1O/w1cDnyilFU='
        secret = 'a4ed35595a910b7ffda8a92723627d47'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型

        if type=='sticker':
            line_bot_api.reply_message(tk,StickerSendMessage(package_id="446", sticker_id="1988"))  #回傳貼圖
            print(123) 
        if type=='image':
            # 回傳圖片
            img_message = ImageSendMessage(
                original_content_url='https://www.starlike.com.tw/wp-content/uploads/2020/06/MIKASA-%E8%B6%85%E7%BA%96%E7%9A%AE%E8%A3%BD%E6%AF%94%E8%B3%BD%E7%B4%9A%E6%8E%92%E7%90%83-%E5%9C%8B%E9%9A%9B%E6%8E%92%E7%B8%BD%E6%AF%94%E8%B3%BD%E6%8C%87%E5%AE%9A%E7%90%83-V200W.png', 
                preview_image_url='https://www.starlike.com.tw/wp-content/uploads/2020/06/MIKASA-%E8%B6%85%E7%BA%96%E7%9A%AE%E8%A3%BD%E6%AF%94%E8%B3%BD%E7%B4%9A%E6%8E%92%E7%90%83-%E5%9C%8B%E9%9A%9B%E6%8E%92%E7%B8%BD%E6%AF%94%E8%B3%BD%E6%8C%87%E5%AE%9A%E7%90%83-V200W.png'
                )
            line_bot_api.reply_message(tk,img_message) # 回傳圖片
            print(456) 
        
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            if msg == "景點推薦":
                print(123)
                weather = Now_weather.weather()
                temperature = Now_weather.temperature()
                #weather = "雨"
                temperature = randrange(15,24)
                arr = np.array([weather])
                #tidal = Now_weather.tidal()
                tidal = randrange(0,2)
                gender = randrange(0,2)
                age = randrange(15,55)
                print(arr,gender,age,tidal,temperature)
                #recommend = XGBOOST_predicted.XGboost_recommend1(arr,gender,age)
                #recommend = XGBOOST_predicted.XGboost_recommend2(arr,gender,age,tidal,temperature)
                recommend = "掌上明珠"
                print(recommend)
                recommend_website,recommend_imgur,recommend_map = Search.Attractions_recommend(recommend)
                #print(recommend_website,recommend_imgur,recommend_map)
                line_bot_api.reply_message(tk,[TextSendMessage("感謝等待\n系統以AI大數據機器學習的方式推薦以下適合您的地點"),
                                                TextSendMessage(str(recommend)),
                                                ImageSendMessage(original_content_url=str(recommend_imgur),preview_image_url=str(recommend_imgur)),
                                                TextSendMessage(recommend_website),
                                                TextSendMessage(recommend_map)
                                                 ])
        if type=='location':
            
            add = json_data['events'][0]['message']['address']  # 取得 LINE 收到的文字訊息
            lat = json_data['events'][0]['message']['latitude']  # 取得 LINE 收到的文字訊息
            lon = json_data['events'][0]['message']['longitude']  # 取得 LINE 收到的文字訊息
            
            '''
            location_message1 = LocationSendMessage(title='my location',
                                                  address=add,
                                                  latitude=lat,
                                                  longitude=lon)
            line_bot_api.reply_message(tk,[location_message1,
                                           TextSendMessage(add),
                                           TextSendMessage(lat),
                                           TextSendMessage(lon)])
            '''
            googlemap_function.googlemap_search(lon,lat)
            
            print(789) 
                
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run()