from flask import Flask, request
#from gevent.pywsgi import WSGIServer
from random import randrange
# 載入 json 標準函式庫，處理回傳的資料格式
import json
# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models.events import PostbackEvent
#from linebot.exceptions import InvalidSignatureError
#from linebot.models import MessageEvent, TextMessage, TextSendMessage 
from linebot.models import *
#from xgboost import XGBClassifier
import pandas as pd
import numpy as np
import csv
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import XGBOOST_predicted
import ML
import Search
import Now_weather
import Filter
import Plan2MYSQL
import FlexMessage
import Googlemap_function
import get_location
import plan_location
import PH_Attractions


app = Flask(__name__)

access_token = 'V4+QzW5Zu+5aqegbPd98R8heE/bit/OZX1WqLCArDIqHHNuH0dPyR4KdNLByK26hc1l+L9N4Vk8DwwDFxeCzS8atb+wTlpsXHSwb5zBEwU39/own3+XL5N6SPWQiFOteHtMMav/uFb1Wu1R5byP/tgdB04t89/1O/w1cDnyilFU='
secret = '1fde7c25c10170fae034fd3bbc495755'
line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
handler = WebhookHandler(secret)                     # 確認 secret 是否正確
PHP_ngrok ="https://3835-140-115-212-35.ngrok-free.app"#80
global age
global gender

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    global approveGender
    global approveAgeRespond

    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            #功能1
            if msg == "行程規劃":
                print(msg)
                line_bot_api.reply_message(tk,[TextSendMessage("請選擇您的行程規劃天數，將以大數據推薦行程"),FlexMessage.travel_reply("行程規劃","兩天一夜","兩天一夜","兩天一夜","三天兩夜","三天兩夜","三天兩夜","四天三夜","四天三夜","四天三夜","五天四夜","五天四夜","五天四夜")])               
            #功能2
            elif msg == "景點推薦":
                print(msg)
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
                recommend = XGBOOST_predicted.XGboost_recommend1(arr,gender,age)
                #recommend = XGBOOST_predicted.XGboost_recommend2(arr,gender,age,tidal,temperature)
                #recommend = "掌上明珠"
                print(recommend)
                recommend_website,recommend_imgur,recommend_map = PH_Attractions.Attractions_recommend(recommend)
                #print(recommend_website,recommend_imgur,recommend_map)
                line_bot_api.reply_message(tk,[TextSendMessage("感謝等待\n系統以AI大數據機器學習的方式推薦以下適合您的地點"),
                                                      TextSendMessage(str(recommend)),
                                                      ImageSendMessage(original_content_url=str(recommend_imgur)+".jpg",preview_image_url=str(recommend_imgur)+".jpg"),
                                                      TextSendMessage(recommend_website),
                                                      TextSendMessage(recommend_map)
                                                      ])
                '''
                recommend_website,recommend_imgur,recommend_map = Search.Attractions_recommend(recommend)
                line_bot_api.reply_message(tk,[TextSendMessage("感謝等待\n系統以AI大數據機器學習的方式推薦以下適合您的地點"),
                                                TextSendMessage(str(recommend)),
                                                ImageSendMessage(original_content_url=str(recommend_imgur),preview_image_url=str(recommend_imgur)),
                                                TextSendMessage(recommend_website),
                                                TextSendMessage(recommend_map)
                                                 ])
                '''                                 
            #功能3
            elif msg == "景點人潮":
                print(msg)
                line_bot_api.reply_message(tk, [TextSendMessage("請點選以下網址，將由大數據為您分析這時間的人潮"),TextSendMessage(str(PHP_ngrok)+"/PengHu/PengHu_crowd2.php")])
            #功能4
            elif msg == "附近搜尋":
                print(msg)
                line_bot_api.reply_message(tk,FlexMessage.ask_location())
            elif msg == "餐廳" or msg == "停車場" or msg == "住宿":
                print(msg)
                lat,lon=get_location.get_location('C:/Users/roy88/testproject/python/PH/location.csv')
                Googlemap_function.googlemap_search_nearby(lat,lon,msg)
                carousel_contents=FlexMessage.Carousel_contents('C:/Users/roy88/testproject/python/PH/recommend.csv')
                line_bot_api.reply_message(tk,FlexMessage.Carousel(carousel_contents)) 
            elif msg == "景點":
                print(msg)                                       # 印出內容
                line_bot_api.reply_message(tk, [TextSendMessage("請點選以下網址，將為您推薦附近景點"),TextSendMessage(str(PHP_ngrok)+"/PengHu/attration_not_trainning.php")])
            #功能5
            elif msg == "租車":
                line_bot_api.reply_message(tk, [TextSendMessage("請點選以下網址，將為您推薦租車店家"),TextSendMessage(str(PHP_ngrok)+"/PengHu/car_rent.php")])
            #功能6
            elif msg == "收集資料&修改資料":
                print(msg)
                line_bot_api.reply_message(tk,TextSendMessage("請輸入你的年紀"))
                approveAgeRespond=True
            elif approveAgeRespond==True:
                try:
                    age=msg #儲存age
                    print("detect age=",age)
                    if 0<=int(age) and int(age)<=120:
                        approveAgeRespond=False
                        message=FlexMessage.gender_reply("性別類型","請輸入您的性別","男","男","男","女","女","女","其他","其他","其他")
                        line_bot_api.reply_message(tk,message)
                        approveGender=True
            
                    #年紀不合常理
                    else:
                        print("data overflow or underflow", age)
                        line_bot_api.reply_message(tk,TextSendMessage("請輸入\"正確年紀\""))
                #其他錯誤
                except Exception as e:
                    print("age type error", age)
                    line_bot_api.reply_message(tk,TextSendMessage("請輸入\"正確年紀\""))
            else :
                print(msg)                                       # 印出內容
                reply = msg
                line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
        
        if type=='location':
            add = json_data['events'][0]['message']['address']  # 取得 LINE 收到的文字訊息
            lat = json_data['events'][0]['message']['latitude']  # 取得 LINE 收到的文字訊息
            lon = json_data['events'][0]['message']['longitude']  # 取得 LINE 收到的文字訊息
            print(add, lat, lon)
            with open('C:/Users/roy88/testproject/python/PH/location.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([add, lat, lon])
            line_bot_api.reply_message(tk,FlexMessage.ask_keyword()) 
            print(789) 

    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

@handler.add(PostbackEvent)
def handle_postback(event):
    # 取得 Postback Action 傳送的資料
    postback_data = event.postback.data
    if postback_data =="兩天一夜":
            print("2days")
            gender = randrange(0,2)
            age = randrange(15,55)
            file='C:/Users/roy88/testproject/python/PH/plan_2day.csv'
            plan_data = pd.read_csv(file,encoding='utf-8-sig')
            userID = ML.XGboost_plan(plan_data,gender,age)  
            print(userID)
            Filter.filter(file,userID)
            Plan2MYSQL.plan2mysql('C:/Users/roy88/testproject/python/PH/plan.csv')
            line_bot_api.reply_message(event.reply_token, [TextSendMessage("以使用機器學習依據相關性，找尋過往數據最適合您的兩天一夜行程"),TextSendMessage(str(PHP_ngrok)+"/PengHu/PengHu_plan.php")])
            
    elif postback_data =="三天兩夜":
            print("3days")
            gender = randrange(0,2)
            age = randrange(15,55)
            file='C:/Users/roy88/testproject/python/PH/plan_3day.csv'
            plan_data = pd.read_csv(file,encoding='utf-8-sig')
            userID = ML.XGboost_plan(plan_data,gender,age)  
            print(userID)
            Filter.filter(file,userID)
            Plan2MYSQL.plan2mysql('C:/Users/roy88/testproject/python/PH/plan.csv')
            line_bot_api.reply_message(event.reply_token, [TextSendMessage("以使用機器學習依據相關性，找尋過往數據最適合您的三天兩夜行程"),TextSendMessage(str(PHP_ngrok)+"/PengHu/PengHu_plan.php")])
    elif postback_data =="四天三夜":
            print("4days")
            gender = randrange(0,2)
            age = randrange(15,55)
            file='C:/Users/roy88/testproject/python/PH/plan_4day.csv'
            plan_data = pd.read_csv(file,encoding='utf-8-sig')
            userID = ML.XGboost_plan(plan_data,gender,age)  
            print(userID)
            Filter.filter(file,userID)
            Plan2MYSQL.plan2mysql('C:/Users/roy88/testproject/python/PH/plan.csv')
            line_bot_api.reply_message(event.reply_token, [TextSendMessage("以使用機器學習依據相關性，找尋過往數據最適合您的四天三夜行程"),TextSendMessage(str(PHP_ngrok)+"/PengHu/PengHu_plan.php")])
    elif postback_data =="五天四夜":
            print("5days")
            gender = randrange(0,2)
            age = randrange(15,55)
            file='C:/Users/roy88/testproject/python/PH/plan_5day.csv'
            plan_data = pd.read_csv(file,encoding='utf-8-sig')
            userID = ML.XGboost_plan(plan_data,gender,age)  
            print(userID)
            Filter.filter(file,userID)
            Plan2MYSQL.plan2mysql('C:/Users/roy88/testproject/python/PH/plan.csv')
            line_bot_api.reply_message(event.reply_token, [TextSendMessage("以使用機器學習依據相關性，找尋過往數據最適合您的五天四夜行程"),TextSendMessage(str(PHP_ngrok)+"/PengHu/PengHu_plan.php")])
    elif postback_data=="男" or postback_data=="女" or postback_data=="其他":
            gender=postback_data
            gender=FlexMessage.classify_gender(gender)
            print(gender)
            line_bot_api.reply_message(event.reply_token,TextSendMessage("資料儲存完畢"))
            print("結束使用\"收集資料功能\" \n------------------")
    if postback_data=="需要幫助" :
        reply_array=[]
        reply_array.append(ImageSendMessage(original_content_url='https://imgur.com/8AKsigL.png',preview_image_url='https://imgur.com/8AKsigL.png'))
        reply_array.append(ImageSendMessage(original_content_url='https://imgur.com/bXnZJLP.png',preview_image_url='https://imgur.com/bXnZJLP.png'))
        reply_array.append(ImageSendMessage(original_content_url='https://imgur.com/QXc788f.png',preview_image_url='https://imgur.com/QXc788f.png'))
        reply_array.append(ImageSendMessage(original_content_url='https://imgur.com/BwqfFxs.png',preview_image_url='https://imgur.com/BwqfFxs.png'))
        line_bot_api.reply_message(event.reply_token,reply_array)
if __name__ == "__main__":
    app.run()