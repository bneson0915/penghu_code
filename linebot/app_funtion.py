from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import configparser
import datetime
import pandas as pd
import json
config=configparser.ConfigParser()
config.read('information.ini')
#first fucntion
def gender_reply(Title,question,label1,text1,data1,label2,text2,data2,label3,text3,data3,event):
    try:
        
        bubble = BubbleContainer(
            direction='ltr',
            #最上層
            hero=ImageComponent(
                    url=config.get('button_pic','gender'),
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover',
            ),
            #中間層
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text=question,size='xl',color='#000000',align='center')
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
                ]
            ),
        )
        message=FlexSendMessage(alt_text=Title,contents=bubble)
        return message
    except:
        print("ERROR")

def travel_reply(Title,question,label1,text1,data1,label2,text2,data2,label3,text3,data3,label4,text4,data4,event):
    try:
        bubble = BubbleContainer(
            direction='ltr',
            #最上層
            hero=ImageComponent(
                    url=config.get('button_pic','trip'),
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover',
            ),
            #中間層
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text=question,size='xl',color='#000000',align='center')
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
        print("ERROR")
'''        
def classify_gender(gender):
    match gender:
        case "男":
            gender=1
        case "女":
            gender=0
        case "其他":
            gender=-1
    return gender
def classify_category(category):
    match category:
        case "情侶":
            category=1
        case "退休族":
            category=2
        case "親子團":
            category=3
        case "朋友團":
            category=4
    return category
'''
def classify_gender(gender):
    if gender=="男":
        gender = 1
    elif gender=="女":
         gender = 0 
    elif gender=="其他":
        gender = -1  
    return gender
def classify_category(category):
    if category =="情侶":
       category =1
    elif category=="退休族":
        category=2  
    elif category=="親子團":
        category=3
    elif category=="朋友團":         
       category=4   
    return category   
                    
def changedataBase(userID,age,gender,category,rain_probability):
    
    df=pd.read_csv("dataCollect_temp.csv")
    repeat=False
    #detect whether database have the same UserID
    for i in range(0,df.shape[0]):
        userID_data=df.at[i,'userID']
        if userID_data==userID:
            repeat=True
            break
    if repeat:
        #replace the previous data
        df.at[i, "age"] = age
        df.at[i,"gender"]=gender
        df.at[i,'category']=category
        df.at[i,'rain_probability']=rain_probability
    else:
        #create the new row
        df=df.append({"userID":userID,
                      "age":age,
                      "gender":gender,
                      "category":category
                      ,"rain_probability": rain_probability},ignore_index=True)
    df.to_csv("dataCollect_temp.csv",index=False) 

#second function
def getCustomerData(userID):
    df=pd.read_csv("dataCollect_temp.csv")
    for i in range(0,df.shape[0]):
        userID_data=df.at[i,'userID']
        if userID_data==userID:
            customerData={
                'age': [df.at[i,'age']],
                'gender': [df.at[i,'gender']],
                'category': [df.at[i,'category']],
                'rain_probability': [df.at[i,'rain_probability']]
            }
            return customerData
    return 0        
def ID_to_locationList(userID,path,duration):
    input_dir = 'C:/Users/ASUS/Desktop/LINE-BOT/'
    df = pd.read_csv(input_dir +path+'.csv')
    location_list=[]
    firstaction=True
    for i in range(0,df.shape[0]):
        #兩個狀況會break
        # 分別是同一ID的時間超過duration
        # 當ID掃描完時
        if userID==df.at[i,"userID"]:
            if firstaction:
                start=datetime.datetime.strptime(df.at[i,"Time"],"%Y/%m/%d %H:%M")
                firstaction=False
            else:
                now=datetime.datetime.strptime(df.at[i,"Time"],"%Y/%m/%d %H:%M")
                if (now-start).days>duration:
                    break
            location=[df.at[i,"設置點"],df.at[i,"緯度"],df.at[i,"經度"]]
            location_list.append(location)
        elif userID!=df.at[i,"userID"] and firstaction==False:
            break
    if firstaction:
        return -1 #can't find 
    else:
        return location_list    
        
def varibleButton(question,viewpoint_list):
    
    try:
        print("景點個數=",len(viewpoint_list))
        if  len(viewpoint_list)%20==0:
            numberOfBubble=int(len(viewpoint_list)/20)
        else:
            numberOfBubble=int(len(viewpoint_list)/20+1)
        
        for j in range(numberOfBubble):
            #因為一個bubble 最高上限是20個，要預防超過二十個的狀況
            buttons=[]
            for i in range(j*20,len(viewpoint_list)):
                button=ButtonComponent(style='secondary',
                                    color='#FFEE99',
                                    height='sm',
                                    action=PostbackAction(label=viewpoint_list[i][0],data=viewpoint_list[i][0],text=viewpoint_list[i][0]) #viewpoint_list[i][0] 是景點的名稱
                                    )
                buttons.append(button)
                buttons.append(SeparatorComponent(color='#000000'))
            bubble = BubbleContainer(
                direction='ltr',
                #最上層
                hero=ImageComponent(
                        url=config.get('button_pic','hotel'),
                        size='full',
                        aspect_ratio='20:13',
                        aspect_mode='cover',
                ),
                #中間層
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(text=question,size='xl',color='#000000',align='center')
                    ],
                ),
                #最下層
                footer=BoxComponent(
                    layout='vertical',
                    spacing='xs', 
                    contents=buttons
                ),
            )
            message=FlexSendMessage(alt_text="Dialog",contents=bubble)
            # message_array.append(message)
        #print("buttons ",buttons)
        return message
    except:
        print("error varibleButton")    
        
def comfirmButton():
    message=TemplateSendMessage(alt_text="ComfirmTemplate",template=ConfirmTemplate(text="請告訴系統您目前的位置",
                                                                            actions=[MessageAction(label="需要幫助",text="需要幫助"),MessageAction(label='好',text='好')]))
    return message

def BubbleSort(list,object):
    list_num=len(list)
    for i in range(list_num):
        for j in range(0,list_num-i-1):
            try:
                if list[j][object]=='N/A' or list[j][object]<list[j+1][object]:
                    list[j],list[j+1]=list[j+1],list[j]
            except Exception:
                continue
    return list

def carousel_adjust(flex_message,search_list,search_number):
    if search_number==0:
        return "Error"
    for i in range(search_number): 
        buttonElement=json.load(open('json/third_function/button_element.json','r',encoding='utf-8'))
        buttonElement['hero']['url']=search_list[i]['url']
        buttonElement['body']['contents'][0]['text']=search_list[i]['name']
        rating=search_list[i]['rating']
        try:
            buttonElement=rating_icon(buttonElement,rating)
        except Exception:
            continue
        buttonElement['body']['contents'][1]['contents'][5]['text']=str(rating)
        buttonElement['body']['contents'][2]['contents'][0]['text']="價格等級: "+str(search_list[i]['price_level'])
        place_id=search_list[i]['place_id']
        buttonElement['footer']['contents'][0]['action']['uri']=f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        flex_message['contents'].append(buttonElement)
    return flex_message

def rating_icon(buttonElement,rating):
    if rating>=1:
        buttonElement['body']['contents'][1]['contents'][0]['url']="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    elif 0.5<=rating:
        buttonElement['body']['contents'][1]['contents'][0]['url']="https://imgur.com/8eAZJ80.png"
        return buttonElement
    if rating>=2:
        buttonElement['body']['contents'][1]['contents'][1]['url']="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    elif 1.5<=rating:
        buttonElement['body']['contents'][1]['contents'][1]['url']="https://imgur.com/8eAZJ80.png"
        return buttonElement
    if rating>=3:
        buttonElement['body']['contents'][1]['contents'][2]['url']="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    elif 2.5<=rating:
        buttonElement['body']['contents'][1]['contents'][2]['url']="https://imgur.com/8eAZJ80.png"
        return buttonElement
    if rating>=4:
        buttonElement['body']['contents'][1]['contents'][3]['url']="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    elif 3.5<=rating:
        buttonElement['body']['contents'][1]['contents'][3]['url']="https://imgur.com/8eAZJ80.png"
        return buttonElement
    if rating>=5:
        buttonElement['body']['contents'][1]['contents'][4]['url']="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    elif 4.5<=rating:
        buttonElement['body']['contents'][1]['contents'][4]['url']="https://imgur.com/8eAZJ80.png"
    return buttonElement