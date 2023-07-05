# -*- coding: utf-8 -*-
### 載入套件
## 載入LineBot所需要的套件
import liffAPI
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from liffpy import LineFrontendFramework as LIFF,ErrorResponse


## 載入flask套件
from flask import Flask, request, abort,jsonify
from flask.helpers import send_file
from flask_cors import CORS

## 載入一般套件
import json
import re
import os

## 載入自己寫的其他py檔案
import searchSQL
import openFile
import richMenu1


### 開始寫程式
## Flask基本設定
app = Flask(__name__)
CORS(app)

## LineBotApi基本設定
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('snfd0pJkVVClMxOZECyIAEVe967tFFD0B7vSQhfy4o8mNxl5K6yF5EG31+kKYiEvqYxWPRnzBqFKGBcForbU6PR51Vc7hJ2neyYE9/b36BRZ/QAFJ+22Zj2+FNn6TBi+duDI7i5ODCYZlcuQB5d//wdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('8fc8ddbdcc4a6e7800953f3b5a177939')
# 必須放上自己的Channel Access Token
liff_api = LIFF('snfd0pJkVVClMxOZECyIAEVe967tFFD0B7vSQhfy4o8mNxl5K6yF5EG31+kKYiEvqYxWPRnzBqFKGBcForbU6PR51Vc7hJ2neyYE9/b36BRZ/QAFJ+22Zj2+FNn6TBi+duDI7i5ODCYZlcuQB5d//wdB04t89/1O/w1cDnyilFU=')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
# Message event
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # profile = line_bot_api.get_profile(event.source.user_id)
    # user_name = profile.display_name
    # message = event.message.text
    userID = event.source.user_id
    userName = line_bot_api.get_profile(userID).display_name
    replyToken = event.reply_token
    receiveMessage = event.message.text

    sqlResult = searchSQL.SQL_getUserStatusAndMarketName(userID)
    marketName = sqlResult[0][0]
    statusID = sqlResult[0][1]

    
    
    if statusID == '1':
        message = TextSendMessage(text="親 請點擊圖文選單")
        line_bot_api.reply_message(replyToken,message)

    elif statusID == '2':
        message = TextSendMessage(f"已幫你變更為查找{receiveMessage}的食材囉")
        line_bot_api.reply_message(replyToken,message)
        searchSQL.SQL_updateUserStatus(userID,'1')

    elif statusID == '3':
        resultList = searchSQL.SQL_getIngreSameCommNameID(receiveMessage)
        if len(resultList) == 0:
            # 沒這東西
            line_bot_api.reply_message(replyToken,"哭阿沒這個食材")
        elif len(resultList) == 1:
            # 看來運氣很好哦 那我就好心幫你Link過去學名吧
            ingreName = resultList[0][1]
            url = richMenu1.getIngredientReportPNG(ingreName,userID)
            print(url)
            reply_arr = []
            message = ImagemapSendMessage(
                base_url= url,
                alt_text= ingreName,
                base_size=BaseSize(height=1024, width=1024),
                )
            reply_arr.append(message)
            message = TextSendMessage(
                text=f"下面連結是Line購物裡的{receiveMessage}，在裡面購買會有Line Point點數回饋歐～ https://buy.line.me/s/{receiveMessage}")
            reply_arr.append(message)
            line_bot_api.reply_message(replyToken, reply_arr)
            searchSQL.SQL_updateUserStatus(userID,'1')
        else:
            # 吃我的選擇學名大禮包
            message = TextSendMessage(text=f"{receiveMessage}有分以下幾項品種，{userName}你想要查詢哪一種呢？",
                                  quick_reply=QuickReply(
                                      items=[
                                          QuickReplyButton(action=MessageAction(label=x[1], text=x[1])) for x in resultList ]))
            line_bot_api.reply_message(replyToken, message)
        

    elif statusID == '4':
        print('4')
    elif statusID == '5':
        print('5')
    elif statusID == '6-1':
        print('6-1')
    elif statusID == '6-2':
        print('6-2')
    elif statusID == '7':
        print('7')
    elif statusID == '8-1':
        searchSQL.SQL_updateUserStatus(userID,'1')
    elif statusID == '8-2':
        searchSQL.SQL_updateUserStatus(userID,'1')
    elif statusID == '8-3':
        print('8-3')
    elif statusID == '8-4':
        print('8-4')
    else:
        print("not found")


# Follow event
@ handler.add(FollowEvent)
def handle_follow(event):
    replyToken = event.reply_token
    userID = event.source.user_id
    userName = line_bot_api.get_profile(userID).display_name
    reply_arr = []
    marketNameListShow = ['北部','中部','南部']
    marketNameList = ['台北一','台中市','高雄市']
    reply_arr.append(TextSendMessage(text=f"Hi！{userName}\n歡迎加入『殺必鼠－智慧食價食材』\n我是您最好的機器人夥伴🤖『阿鼠－殺必鼠』🐭🐭\n每天都將提供您市場最新的菜價優惠\n不只如此，還能為您訂做一系列的菜單\n\n自從殺必鼠本人知道最新菜價後\n去菜市場買菜都不會被老闆哄抬價格\n從原本的月底「吃土」改成「吃菜」過生活\n殺必鼠本人用過就回不去了\n真心推薦"))
    reply_arr.append(TextSendMessage(text=f"請問{userName}想要查詢北、中、南哪個地區的食材價格呢？",
                                        quick_reply=QuickReply(
                                        items=[
                                          QuickReplyButton(action=PostbackAction(
                                              label=marketNameListShow[i], 
                                              text=marketNameListShow[i] ,
                                              data=f'&statusCode=2&地區={marketNameList[i]}&表面地區={marketNameListShow[i]}&')) for i in range(3) ])))
    #reply_arr.append(buttons_template_message)

    line_bot_api.reply_message(replyToken, reply_arr)


# PostbackEvent
@ handler.add(PostbackEvent)
def handle_follow(event):
    data = event.postback.data
    replyToken = event.reply_token
    userID = event.source.user_id
    userName = line_bot_api.get_profile(userID).display_name
    if 'statusCode' in data:
        statusID = data.split('statusCode=',1)[1].split('&',1)[0]
    if '地區' in data:
        marketName = data.split('地區=',1)[1].split('&',1)[0]
        

    statusIDList = ['1','2','3','4','5','6-1','6-2','7','8-1','8-2','8-3','8-4']
    for i in statusIDList:
        if statusID == i:
            searchSQL.SQL_updateUserStatus(userID,statusID)

    if statusID == '2':
        searchSQL.SQL_updateUserMarketName(userID,marketName)

    if statusID == '3':
        message = TextSendMessage(f"{userName}今天想要查詢什麼食材呢？")
        line_bot_api.reply_message(replyToken,message)
    
    if statusID == '8-1':
        message = TextSendMessage(text=f"{userName}，你遇到什麼問題了嗎？",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="新手教學", text="新手教學",data="&statusCode=8-2&")),
                        QuickReplyButton(
                            action=URIAction(label="設定厭世食材",uri='https://liff.line.me/1656748829-9amYlYbd')),
                        QuickReplyButton(
                            action=PostbackAction(label="更改地區", text="更改地區",data='&statusCode=8-3&')),
                        QuickReplyButton(
                            action=PostbackAction(label="Q&A", text="Q&A",data='&statusCode=8-4'))]))
        line_bot_api.reply_message(replyToken, message)

    if statusID == '7':
        reply_arr = []
        ingreList= ['雞肉','高麗菜','青蔥']
        menu1 = openFile.openMenuJson('雞肉')
        menu2 = openFile.openMenuJson('高麗菜')
        menu3 = openFile.openMenuJson('青蔥')
        message = FlexSendMessage(
            alt_text='好康嚴選清單',
            contents={
                "type": "carousel",
                "contents": [
                    menu1,
                    menu2,
                    menu3,
                ]
            }
        )
        reply_arr.append(message)
        message = TemplateSendMessage(
            alt_text='好康嚴選圖片',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/yeLuhGt.jpg',
                        action=URITemplateAction(
                            uri='https://i.imgur.com/yeLuhGt.jpg'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/G7MOPDc.png',
                        action=URITemplateAction(
                            uri='https://i.imgur.com/G7MOPDc.png'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/NrO9Ls2.jpg',
                        action=URITemplateAction(
                            uri='https://i.imgur.com/NrO9Ls2.jpg'
                        )
                    )
                ]
            )
        )
        reply_arr.append(message)
        url = 'https://today.line.me/tw/v2/article/7rvnGJ'
        message = TextSendMessage("讓我們一起幫助辛苦的農民吧！\n"+url)
        reply_arr.append(message)
        line_bot_api.reply_message(replyToken, reply_arr)
    if statusID == '8-2':
        marketNameListShow = ['北部','中部','南部']
        marketNameList = ['台北一','台中市','高雄市']
        message = TextSendMessage(text=f"請問{userName}想要查詢北、中、南哪個地區的食材價格呢？",
                                    quick_reply=QuickReply(
                                    items=[
                                          QuickReplyButton(action=PostbackAction(
                                              label=marketNameListShow[i], 
                                              text=marketNameListShow[i] ,
                                              data=f'&statusCode=2&地區={marketNameList[i]}&表面地區={marketNameListShow[i]}&')) for i in range(3) ]))
        line_bot_api.reply_message(replyToken,message)

# request大圖選單
@app.route("/ingredient/richMenu/<imageID>.png/1040")
def get_bigmap1040(imageID):
    dirPath = os.path.dirname(__file__) + '/response_LineBot/menuBtn1/{}.png'
    try:
        return send_file(dirPath.format(imageID),mimetype="image/png")
    except:
        return send_file(dirPath.format(imageID),mimetype="image/png")

# request大圖選單
@app.route("/ingredient/richMenu/<imageID>.png/700")
def get_bigmap700(imageID):
    dirPath = os.path.dirname(__file__) + '/response_LineBot/menuBtn1/{}.png'
    try:
        return send_file(dirPath.format(imageID),mimetype="image/png")
    except:
        return send_file(dirPath.format(imageID),mimetype="image/png")

## 以下為LIFF專區
@app.route('/')
def index():
    return 'Not Hello World!'

# request每張食材的圖片
@app.route("/ingredient/photo/<imageID>.jpg")
def get_photo(imageID):
    dirPath = os.path.dirname(__file__) + '/ingredient_picture/{}.jpg'
    try:
        return send_file(dirPath.format(imageID),mimetype="image/jpg")
    except:
        return send_file(dirPath.format('FA800'),mimetype="image/jpg")
    # with open(dirPath.format(imageID),'rb') as fp:
    #     image = fp.read()
    #     resp = Response(image,mimetype="image/jpg")
    #     return resp

@app.route('/ingredient/')
def getALLingredient():
    userID = request.args.get('userID')
    response = liffAPI.responseIngredient(userID)
    return response


@app.route('/sendUnlikeJson',methods=['GET','POST'])
def unlikeJson():
    if request.method == 'GET':
        return "母湯哦怎麼可以用 request.get 摁?"
    else:
        data = json.loads(request.get_data())
        userID = data['userID']
        token = data['token']
        unlikeIngredientID = data['unlikeIngredientID']
        responses = liffAPI.updateUserUnlike(userID,token,unlikeIngredientID)
        return responses


# 主程式
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5001,
        ssl_context=('./conf/ssl.crt/server.crt', './conf/ssl.key/server.key')
    )
