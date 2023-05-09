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
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import ML
import Search
import Now_weather
import Filter

app = Flask(__name__)

access_token = '9L8HgvDkVZgSZZy6S9ihK2r/6UJv5miDFNjHJt0FKfs4yITvDESQAKhiKAyLIAWK8Kjn55api/1/25vC8aceJUhjr23DfqJsxkIJuYH6v7gHjRRzRSHssanGqt873C6i8rp9BxmT4BsrMILekVSppwdB04t89/1O/w1cDnyilFU='
secret = 'a4ed35595a910b7ffda8a92723627d47'
line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
handler = WebhookHandler(secret)                     # 確認 secret 是否正確
PHP_ngrok = ""

def travel_reply(Title,label1,text1,data1,label2,text2,data2,label3,text3,data3,label4,text4,data4):
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        
        bubble = BubbleContainer(
            direction='ltr',
            #最上層
            hero=ImageComponent(
                    url='https://i.imgur.com/W7kiWQT.png',
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover',
            ),
            #中間層
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text="請選擇您的行程規劃天數",size='xl',color='#000000')
                ],
            ),
            #最下層
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=PostbackAction(label=label1,text=text1,data=data1)
                    ),
                    SeparatorComponent(color='#000000'),
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=PostbackAction(label=label2,text=text2,data=data2)#(一定要有label和data)data設定為傳到handle_postback的值，text為使用者這邊跳出的文字
                    ),
                    SeparatorComponent(color='#000000'),
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=PostbackAction(label=label3,text=text3,data=data3)#(一定要有label和data)data設定為傳到handle_postback的值，text為使用者這邊跳出的文字
                    ),
                    SeparatorComponent(color='#000000'),
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=PostbackAction(label=label4,text=text4,data=data4)#(一定要有label和data)data設定為傳到handle_postback的值，text為使用者這邊跳出的文字
                    )
                ]
            ),
        )
        message=FlexSendMessage(alt_text=Title,contents=bubble)
        return message
    except:
         line_bot_api.reply_message(tk,TextSendMessage("發生錯誤"))

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            if msg == "行程規劃":
                print(888)
                line_bot_api.reply_message(tk,[TextSendMessage("請選擇您的行程規劃天數，將以大數據推薦行程"),travel_reply("行程規劃","兩天一夜","兩天一夜","兩天一夜","三天兩夜","三天兩夜","三天兩夜","四天三夜","四天三夜","四天三夜","五天四夜","五天四夜","五天四夜")])               
            elif msg == "景點推薦":
                print(123)
                weather = Now_weather.weather()
                temperature = Now_weather.temperature()
                #weather = "雨"
                #temperature = randrange(15,24)
                arr = np.array([weather])
                tidal = Now_weather.tidal()
                #tidal = 0
                gender = randrange(0,2)
                age = randrange(15,55)
                print(arr,gender,age,tidal,temperature)
                recommend = ML.XGboost_recommend1(arr,gender,age)
                #recommend = ML.XGboost_recommend2(arr,gender,age,tidal,temperature)
                print(recommend)
                recommend_website,recommend_imgur,recommend_map = Search.Attractions_recommend(recommend)
                #print(recommend_website,recommend_imgur,recommend_map)
                line_bot_api.reply_message(tk,[TextSendMessage("感謝等待\n系統以AI大數據機器學習的方式推薦以下適合您的地點"),
                                                TextSendMessage(str(recommend)),
                                                ImageSendMessage(original_content_url=str(recommend_imgur),preview_image_url=str(recommend_imgur)),
                                                TextSendMessage(recommend_website),
                                                TextSendMessage(recommend_map)
                                                 ])
            #elif msg == "景點推薦":
            #    line_bot_api.reply_message(event.reply_token, [TextSendMessage("請點選以下網址，將由大數據為您分析這時間的人潮"),TextSendMessage(str(PHP_ngrok)+"/PengHu_crowd.php")])
            else :
                print(msg)                                       # 印出內容
                reply = msg
                line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
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
            line_bot_api.reply_message(event.reply_token, [TextSendMessage("以使用機器學習依據相關性，找尋過往數據最適合您的兩天一夜行程"),TextSendMessage(str(PHP_ngrok)+"/PengHu_plan.php")])        
    elif postback_data =="三天兩夜":
            print("3days")
            gender = randrange(0,2)
            age = randrange(15,55)
            file='C:/Users/roy88/testproject/python/PH/plan_3day.csv'
            plan_data = pd.read_csv(file,encoding='utf-8-sig')
            userID = ML.XGboost_plan(plan_data,gender,age)  
            print(userID)
            Filter.filter(file,userID)
            line_bot_api.reply_message(event.reply_token, [TextSendMessage("以使用機器學習依據相關性，找尋過往數據最適合您的三天兩夜行程"),TextSendMessage(str(PHP_ngrok)+"/PengHu_plan.php")])        
    elif postback_data =="四天三夜":
            print("4days")
            gender = randrange(0,2)
            age = randrange(15,55)
            file='C:/Users/roy88/testproject/python/PH/plan_4day.csv'
            plan_data = pd.read_csv(file,encoding='utf-8-sig')
            userID = ML.XGboost_plan(plan_data,gender,age)  
            print(userID)
            Filter.filter(file,userID)
            line_bot_api.reply_message(event.reply_token, [TextSendMessage("以使用機器學習依據相關性，找尋過往數據最適合您的四天三夜行程"),TextSendMessage(str(PHP_ngrok)+"/PengHu_plan.php")])        
    elif postback_data =="五天四夜":
            print("5days")
            gender = randrange(0,2)
            age = randrange(15,55)
            file='C:/Users/roy88/testproject/python/PH/plan_5day.csv'
            plan_data = pd.read_csv(file,encoding='utf-8-sig')
            userID = ML.XGboost_plan(plan_data,gender,age)  
            print(userID)
            Filter.filter(file,userID)
            line_bot_api.reply_message(event.reply_token, [TextSendMessage("以使用機器學習依據相關性，找尋過往數據最適合您的五天四夜行程"),TextSendMessage(str(PHP_ngrok)+"/PengHu_plan.php")])        

if __name__ == "__main__":
    app.run()