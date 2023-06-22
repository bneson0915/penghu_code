from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage ,ImageSendMessage
import random
import cv2
import base64
import os, sys
import configparser
import app_funtion
import web_crawler_function
app = Flask(__name__)


# 檢查token是否正確
config = configparser.ConfigParser()
config.read('information.ini')
line_bot_api = LineBotApi('9RuNvHM8Lhh+j7bRhi9E5LUX/YLtEGaKC6IVDDBh1aseFLkGutG3WcteLgpGCKA5ZO6BCARir+IzhLANLFpkBhmiMKTOYaKqy+lW3fyxFFDhHLbbNhHrgOtcdoR5rF5u2qgIcWnFktvOBcoBC8tcSwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('69f1d8d85b8ff0554b4c675482c02ac4')

#檢查linebot資料是否正確
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'
#global varible for the first function 
approveGender=False
approveAgeRespond=False
approveCategory=False
#global varible for the second function
customerData=0 
viewpoint_url="https://4608-220-134-27-198.ngrok-free.app"
viewpoint_list=[]
#global varible for the third function 
approveLocation=False
approveSearchNearby=False
approveAgain=False


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    #global varibles for the first function
        #global variables make sure the information won't create error.
    global approveGender
    global approveAgeRespond
    global approveCategory
    global approveLocation
    global userID
    global age
    global gender
    global category
    global rain_probability
    #global varibles for the second function
    global customerData
    tk=event.reply_token
    msg=event.message.text
    print("obtain text message")
    # first function
    if msg=="收集資料&更改資料":
        line_bot_api.reply_message(tk,TextSendMessage("請輸入你的年紀"))
        approveAgeRespond=True
        userID=event.source.user_id
        print("+++++++++++++++++++\n開始使用\"收集資料功能\" userID= ",userID)
    #儲存age並詢問gender
    elif approveAgeRespond==True:
        #確認是否輸入的是年紀
        try:
            
            age=msg #儲存age
            print("detect age=",age)
            if 0<=int(age) and int(age)<=120:
                approveAgeRespond=False
                message=app_funtion.gender_reply("性別類型","請輸入您的性別","男","男","男","女","女","女","其他","其他","其他",event)
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

    #儲存gender並詢問團體類型
    elif approveGender==True:
        #儲存gender
        print("性－別為：",msg)
        gender=msg
        #確認是否輸入正確
        if gender=="男" or gender=="女" or gender=="其他":
            approveGender=False
            #transform gender from string to int
            gender=app_funtion.classify_gender(gender)
            print(gender)
            message=app_funtion.travel_reply("團體類型","請輸入這次出遊的團體類型","親子團","親子團","親子團","退休族","退休族","退休族","朋友團","朋友團","朋友團","情侶","情侶","情侶",event)
            line_bot_api.reply_message(tk,message)
            approveCategory=True
        #輸入錯誤
        else:
            print("gender input error", age)
            message=app_funtion.gender_reply("性別類型","請重新輸入您的性別","男","男","男","女","女","女","其他","其他","其他",event)
            line_bot_api.reply_message(tk,message)
    elif approveCategory==True:
        #儲存團體類型
        category=msg
        #確認是否輸入正確
        if category=="親子團" or category=="退休族" or category=="朋友團" or category=="情侶":
            approveCategory=False
            #transform category from string to int
            category=app_funtion.classify_category(category)
            print(category)
            #obtain rain_probability
            rain_probability=web_crawler_function.search_rain()
            #save the userID
            app_funtion.changedataBase(event.source.user_id,age,gender,category,rain_probability)
            #回傳收集完畢訊息
            line_bot_api.reply_message(tk,TextSendMessage("資料儲存完畢，可點選\"行程規劃\"開始安排"))
            print("結束使用\"收集資料功能\" \n------------------")
        else:
            print("category input error", age)
            message=app_funtion.travel_reply("團體類型","請重新輸入旅遊類型","親子團","親子團","親子團","退休族","退休族","退休族","朋友團","朋友團","朋友團","情侶","情侶","情侶",event)
            line_bot_api.reply_message(tk,message)
            
    #second fucntion
    elif msg=="行程規劃":
        customerData=app_funtion.getCustomerData(event.source.user_id)
        if customerData:
            #回傳幾天幾夜按鈕
            message=app_funtion.travel_reply("行程規劃","請選擇您的行程規劃天數","兩天一夜","兩天一夜","兩天一夜","三天兩夜","三天兩夜","三天兩夜","四天三夜","四天三夜","四天三夜","五天四夜","五天四夜","五天四夜",event)
            line_bot_api.reply_message(tk,message)
        else:
            line_bot_api.reply_message(tk,TextSendMessage('請點選左下角的\"收集資料&更改資料\"輸入個人資料，系統才能進行分析'))
    # third function
    elif msg=="附近搜尋":
        approveLocation=True
        message=app_funtion.comfirmButton()
        line_bot_api.reply_message(tk,message)
    elif msg=="需要幫助" and approveLocation:
        reply_array=[]
        reply_array.append(ImageSendMessage(original_content_url=config.get('image_url','step1'),preview_image_url=config.get('image_url','step1')))
        reply_array.append(ImageSendMessage(original_content_url=config.get('image_url','step2'),preview_image_url=config.get('image_url','step2')))
        reply_array.append(ImageSendMessage(original_content_url=config.get('image_url','step3'),preview_image_url=config.get('image_url','step3')))
        reply_array.append(ImageSendMessage(original_content_url=config.get('image_url','step4'),preview_image_url=config.get('image_url','step4')))
        line_bot_api.reply_message(tk,reply_array)
if __name__ == "__main__":
    app.run(port=8000)