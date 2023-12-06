# penghu_code
penghu_code 2023
# PengHu_Project
#### 模擬情境:
本研究透過大數據分析針對使用者的個人資訊，以機器學習的方式分析過往遊客的旅遊經驗及當天資訊，提出景點推薦、行程規劃、景點人潮三項功能並建置於Line Bot上，使用者點選欲使用之服務後，根據不同的服務類型，後臺會透過手機端傳回來的使用者資訊，利用機器學習進行計算，並於手機端顯示出與使用者關聯性最高的結果，過程中使用者不需要輸入資料，只需點選按鈕即可完成操作，透過所建置的功能以提供遊客個人化的旅遊規劃服務，解決現有平台旅遊資訊複雜、熱門景點與行程單調、景點人潮難以取得等問題，使用者不需用額外下載應用程式即可規劃出適合自己的行程。  
> 以下為整體架構圖:  
![https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E7%B3%BB%E7%B5%B1%E6%9E%B6%E6%A7%8B%E5%9C%96.png](https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E7%B3%BB%E7%B5%B1%E6%9E%B6%E6%A7%8B%E5%9C%96.png)  

***
## 第一項功能 : 行程規劃
首先資料處理部份我們會依據使用者在澎湖旅遊的天數進行分類。當使用者點選行程規劃的按鈕後，Line Bot 會回傳一份按鈕選單供使用者選擇要到澎湖旅遊的天數，使用者透過按鈕選擇心儀的遊玩天數時，後端系統會立即將使用者的個人化資訊透過機器學習預先於資料庫數據訓練出的模型進行預測，推薦出一段適合使用者的行程路線規畫且顯示於我們所製作的動態網頁，並即時由Line Bot 回傳網頁的網址，以提供使用者一段適合自己的行程規劃。  
### 架構圖 :  
![https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E8%A1%8C%E7%A8%8B%E8%A6%8F%E5%8A%83%E6%9E%B6%E6%A7%8B%E5%9C%96.png](https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E8%A1%8C%E7%A8%8B%E8%A6%8F%E5%8A%83%E6%9E%B6%E6%A7%8B%E5%9C%96.png)  
### 結果圖 :  
![https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E8%A1%8C%E7%A8%8B%E8%A6%8F%E5%8A%83%E7%B5%90%E6%9E%9C%E5%9C%96.png](https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E8%A1%8C%E7%A8%8B%E8%A6%8F%E5%8A%83%E7%B5%90%E6%9E%9C%E5%9C%96.png)  
***
## 第二項功能 : 景點推薦
使用者點選景點推薦功能按鈕後，後端會自行將使用者的個人化數據經過機器學習預先訓練好的模型進行預測，以得到過往大數據統計內，和使用者關聯度最高的遊客所去過的景點，並將此景點與景點的相關資訊 ( 如 : 圖片、網址、導航地圖…等 ) 透過Line Bot推送給使用者，並即時呈現於畫面上，提供使用者一個適合自己遊玩的景點。  
### 架構圖 :  
![https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E6%99%AF%E9%BB%9E%E6%8E%A8%E8%96%A6%E6%9E%B6%E6%A7%8B%E5%9C%96.png](https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E6%99%AF%E9%BB%9E%E6%8E%A8%E8%96%A6%E6%9E%B6%E6%A7%8B%E5%9C%96.png)  
### 結果圖 :  
![https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E6%99%AF%E9%BB%9E%E6%8E%A8%E8%96%A6%E7%B5%90%E6%9E%9C%E5%9C%96.png](https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E6%99%AF%E9%BB%9E%E6%8E%A8%E8%96%A6%E7%B5%90%E6%9E%9C%E5%9C%96.png)  
***
## 第三項功能 : 景點人潮
首先我們會先將過往的數據依照時間段切分為24個資料集，並設計不同的資料表儲存於資料庫內，當使用者點選景點人潮按鈕時，後端系統會即時抓取使用者當下的時間，並自動對應資料庫裡的資料表，將過往當下時間的人流數據顯示於我們所製作的動態網頁上，並由Line Bot 回傳網頁的網址，使用者點選網址後即可看到過往這個時間下的人潮量，能讓使用者避開人流眾多的地區，能更好的安排行程。  
### 架構圖 :  
![https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E6%99%AF%E9%BB%9E%E4%BA%BA%E6%BD%AE%E6%9E%B6%E6%A7%8B%E5%9C%96.png](https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E6%99%AF%E9%BB%9E%E4%BA%BA%E6%BD%AE%E6%9E%B6%E6%A7%8B%E5%9C%96.png)  
### 結果圖 :  
![https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E6%99%AF%E9%BB%9E%E4%BA%BA%E6%BD%AE%E7%B5%90%E6%9E%9C%E5%9C%96.png](https://github.com/ChuJacky0327/PengHu_Project/blob/main/image/%E6%99%AF%E9%BB%9E%E4%BA%BA%E6%BD%AE%E7%B5%90%E6%9E%9C%E5%9C%96.png)  
***
## 備註 :  
> 1. 執行的 python 程式在 **script 資料夾**裡。
> 2. 請事先自行安裝好 **ngrok** 與 **xampp**。
> 3. xampp 預安裝位置為 **C槽**，將此資料夾裡的 **PHP 檔案**放置於 **C:/xampp/htdocs** 裡，開啟 xampp 後，即可在網站輸入 ```http://localhost/XXX.php``` 開啟所需的 PHP 檔。
> 4. 本研究有建構自己的本地資料庫 (MySQL) ，因此 PHP 檔所產生的地圖資訊，是去讀本地資料庫的數據。
> 5. 會利用 ngrok 跳轉 PHP localhost 端的問題，而 ngrok 要同時開啟 port 8000 (給 Line Bot) 和 port 80 (給 PHP 動態網頁)，因此要設成多開 port， 到 ```/Users/XXX/.ngrok2/ngrok.yml```裡新增程式碼。
```shell
tunnels:
  line-bot:
    addr: 8000
    proto: http
    host_header: localhost
    bind_tls: true
  xampp:
    addr: 80
    proto: http
    host_header: localhost:80
    bind_tls: true
```
> 6. ngrok 的指令要下 ```ngrok start --all```，就能透過 **[ngrok網址]/XXX.php** 進到 PHP 網頁並同時使用 Line Bot。
> 7. imgur 禁止了 127.0.0.1 的訪問，所以要測試要用輸入 ```localhost``` 不能用 127.0.0.1。  
> 8. 請先安裝 requirement.txt 的套件 pip install -r requirements.txt
**本專案投稿至 2022智慧物聯網產學研討會**   

