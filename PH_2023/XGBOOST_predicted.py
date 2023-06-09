import xgboost as xgb
import Now_weather
from random import randrange
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

def XGboost_recommend1(arr,gender,age): 
    le = LabelEncoder()
    labelencoder = LabelEncoder()

    Data = pd.read_csv('C:/Users/roy88/testproject/python/xgboost/penghu_orignal2.csv',encoding='utf-8-sig')
    df_data = pd.DataFrame(data= np.c_ [Data['weather'], Data['gender'], Data['age'], Data['設置點']],
                            columns= ['weather','gender','age','label'])
        
    df_data['weather'] = labelencoder.fit_transform(df_data['weather'])#轉換文字要做one-hot encode前要先做label encode

    X = df_data.drop(labels=['label'],axis=1).values # 移除label並取得剩下欄位資料

    onehotencoder = OneHotEncoder(categories = 'auto')
    X=onehotencoder.fit_transform(X).toarray()    
        #print(list(X.columns))
        #R = pd.DataFrame(X)
        #print(R)
    Y = df_data['label'].values    
        
        
    Y = le.fit_transform(Y) #由於字串無法做訓練，所以進行Label encoding編碼

    arr_labelencode = labelencoder.transform(arr) #用同一個labelencoder能transform到一樣的編碼
    #print(arr_labelencode[0])

    Value_arr = np.array([arr_labelencode[0],gender,age])
    #print(Value_arr)
    final=onehotencoder.transform([Value_arr])#用同一個onehotencoder能transform到一樣的編碼
    #print(final)
    loaded_model = XGBClassifier()
    loaded_model.load_model('xgb_model1.bin')
    predicted = loaded_model.predict(final)
    #print(predicted)
    result = le.inverse_transform(predicted)
    #print(result[0])
    return result[0]

def XGboost_recommend2(arr,gender,age,tidal,temperature): 
    le = LabelEncoder()
    labelencoder = LabelEncoder()

    Data = pd.read_csv('C:/Users/roy88/testproject/python/xgboost/penghu_orignal2.csv',encoding='utf-8-sig')
    df_data = pd.DataFrame(data= np.c_ [Data['weather'], Data['gender'], Data['age'] ,Data['tidal'],Data['temperature'],Data['設置點']],
                           columns= ['weather','gender','age','tidal','temperature','label'])
        
    df_data['weather'] = labelencoder.fit_transform(df_data['weather'])#轉換文字要做one-hot encode前要先做label encode

    X = df_data.drop(labels=['label'],axis=1).values # 移除label並取得剩下欄位資料

    onehotencoder = OneHotEncoder(categories = 'auto')
    X=onehotencoder.fit_transform(X).toarray()    
        #print(list(X.columns))
        #R = pd.DataFrame(X)
        #print(R)
    Y = df_data['label'].values    
        
        
    Y = le.fit_transform(Y) #由於字串無法做訓練，所以進行Label encoding編碼

    arr_labelencode = labelencoder.transform(arr) #用同一個labelencoder能transform到一樣的編碼
    #print(arr_labelencode[0])

    Value_arr = np.array([arr_labelencode[0],gender,age,tidal,temperature])
    #print(Value_arr)
    final=onehotencoder.transform([Value_arr])#用同一個onehotencoder能transform到一樣的編碼
    #print(final)
    loaded_model = XGBClassifier()
    loaded_model.load_model('xgb_model2.bin')
    predicted = loaded_model.predict(final)
    #print(predicted)
    result = le.inverse_transform(predicted)
    #print(result[0])
    return result[0]

#arr = np.array("風")
#arr = np.atleast_1d(arr)
#print(XGboost_recommend2(arr,1,25,2,24))
#print(XGboost_recommend1(arr,1,69))
weather = Now_weather.weather()
arr = np.array([weather])
gender = randrange(0,2)
age = randrange(15,55)
temperature = Now_weather.temperature()
tidal = 0
#print(XGboost_recommend1(arr,gender,age))
#print(XGboost_recommend2(arr,gender,age,tidal,temperature))