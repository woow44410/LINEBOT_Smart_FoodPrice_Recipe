# -*- coding: utf-8 -*-
# 載入LineBot所需要的套件
import json
import os

from requests.api import get
import openFile
from flask import Flask, request, abort
from flask import jsonify
from flask.helpers import send_file
import liffAPI

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from liffpy import (
    LineFrontendFramework as LIFF,
    ErrorResponse
)
from flask_cors import CORS


import re

app = Flask(__name__)
CORS(app)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'snfd0pJkVVClMxOZECyIAEVe967tFFD0B7vSQhfy4o8mNxl5K6yF5EG31+kKYiEvqYxWPRnzBqFKGBcForbU6PR51Vc7hJ2neyYE9/b36BRZ/QAFJ+22Zj2+FNn6TBi+duDI7i5ODCYZlcuQB5d//wdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('8fc8ddbdcc4a6e7800953f3b5a177939')
# 早安你好
# line_bot_api.push_message('Uef109eed1fa0684b6c748f6e4b020757', TextSendMessage(text='本地端版本gogo'))

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    message = text = event.message.text
    if re.match("北部", message):
        reply_arr = []
        message = TextSendMessage(text='好的沈翔，之後如果想更改地區的話記得點更多功能喔')
        reply_arr.append(message)
        message = TextSendMessage(text='那就事不宜遲，讓我們先點擊查詢食材價格吧～')
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("中部", message):
        reply_arr = []
        message = TextSendMessage(text='好的沈翔，之後如果想更改地區的話記得點更多功能喔')
        reply_arr.append(message)
        message = TextSendMessage(text='那就事不宜遲，讓我們先點擊查詢食材價格吧～')
        reply_arr.append(message)       
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("南部", message):
        reply_arr = []
        message = TextSendMessage(text='好的沈翔，之後如果想更改地區的話記得點更多功能喔')
        reply_arr.append(message)
        message = TextSendMessage(text='那就事不宜遲，讓我們先點擊查詢食材價格吧～')
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("查詢食材價格", message):
        message = TextSendMessage(text="請問沈翔想要查詢哪種食材呢？")
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("高麗菜", message):
        reply_arr = []
        message = ImagemapSendMessage(
            base_url='https://i.imgur.com/ognPd9g.png',
            alt_text='高麗菜',
            base_size=BaseSize(height=1024, width=1024),
            actions=[
                URIImagemapAction(  # 超連結
                    link_uri='https://icook.tw/recipes/160478',
                    area=ImagemapArea(x=98, y=860, width=255, height=95)
                ),
                URIImagemapAction(  # 超連結
                    link_uri='https://icook.tw/recipes/278462',
                    area=ImagemapArea(x=400, y=860, width=255, height=95)
                ),
                URIImagemapAction(  # 超連結
                    link_uri='https://icook.tw/recipes/393729',
                    area=ImagemapArea(x=688, y=860, width=255, height=95)
                )
            ]
        )
        reply_arr.append(message)
        message = TextSendMessage(
            text="下面連結是Line購物裡的高麗菜，在裡面購買會有Line Point點數回饋歐～ https://buy.line.me/s/%E9%AB%98%E9%BA%97%E8%8F%9C")
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("甘藍", message):
        message = TextSendMessage(text="甘藍有分以下幾項品種，沈翔你想要查詢哪一種呢？",
                                  quick_reply=QuickReply(
                                      items=[
                                          QuickReplyButton(
                                              action=MessageAction(label="高麗菜", text="高麗菜")),
                                          QuickReplyButton(
                                              action=MessageAction(label="花椰菜", text="花椰菜")),
                                          QuickReplyButton(
                                              action=MessageAction(label="芥藍菜", text="芥藍菜")),
                                          QuickReplyButton(
                                              action=MessageAction(label="大頭菜", text="大頭菜"))]))
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("花椰菜", message):
        reply_arr = []
        message = ImagemapSendMessage(
            base_url='https://i.imgur.com/Awnpyid.png',
            alt_text='花椰菜',
            base_size=BaseSize(height=1024, width=1024),
            actions=[
                URIImagemapAction(  # 超連結
                    link_uri='https://icook.tw/recipes/393256',
                    area=ImagemapArea(x=98, y=860, width=255, height=95)
                ),
                URIImagemapAction(  # 超連結
                    link_uri='https://icook.tw/recipes/392055',
                    area=ImagemapArea(x=400, y=860, width=255, height=95)
                ),
                URIImagemapAction(  # 超連結
                    link_uri='https://icook.tw/recipes/388582',
                    area=ImagemapArea(x=688, y=860, width=255, height=95)
                )
            ]
        )
        reply_arr.append(message)
        message = TextSendMessage(
            text="下面連結是Line購物裡的花椰菜，在裡面購買會有Line Point點數回饋歐～ https://buy.line.me/s/%E8%8A%B1%E6%A4%B0%E8%8F%9C")
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("豬腳", message):
        message = TextSendMessage(text="由於豬肉價格比目前平均高出15%，因此較不推薦購買")
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("幫我想菜單", message):
        reply_arr = []
        menu1 = openFile.openMenuJson('銀芽炒雙蔬')
        menu2 = openFile.openMenuJson('糖醋蛋')
        menu3 = openFile.openMenuJson('金菇豆皮')
        menu4 = openFile.openMenuJson('鹽焗蝦')
        menu5 = openFile.openMenuJson('香烤雞腿')
        message = FlexSendMessage(
            alt_text='幫我想菜單',
            contents={
                "type": "carousel",
                "contents": [
                    menu1,
                    menu2,
                    menu3,
                    menu4,
                    menu5
                ]
            }  # json貼在這裡
        )
        reply_arr.append(message)
        message = TextSendMessage(text='沈翔，這邊推薦的食譜如上呦~',
                                  quick_reply=QuickReply(
                                      items=[QuickReplyButton(action=MessageAction(label="重新推薦", text="重新推薦"))]))
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("指定食材食譜", message):
        message = TextSendMessage(text="沈翔你今天想料理哪樣食材呢？")
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("杏鮑菇", message):
        reply_arr = []
        menu1 = openFile.openMenuJson('油菜炒杏鮑菇')
        menu2 = openFile.openMenuJson('椒鹽杏鮑菇')
        menu3 = openFile.openMenuJson('干煸杏鮑菇')
        menu4 = openFile.openMenuJson('蒜香奶油杏鮑菇')
        menu5 = openFile.openMenuJson('偽干貝杏鮑菇')
        message = FlexSendMessage(
            alt_text='杏鮑菇菜單',
            contents={
                "type": "carousel",
                "contents": [
                    menu1,
                    menu2,
                    menu3,
                    menu4,
                    menu5
                ]
            }  # json貼在這裡
        )
        reply_arr.append(message)
        message = TextSendMessage(text='以上是有關杏鮑菇的食譜喔',
                                  quick_reply=QuickReply(
                                      items=[QuickReplyButton(action=MessageAction(label="重新推薦", text="重新推薦：杏鮑菇"))]))
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("指定金額範圍", message):
        message = TextSendMessage(text="沈翔你的總預算是多少呢？輸入範例：0~500")
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("0~500", message):
        message = TextSendMessage(text="那是幾個人要一起享用呢？\n輸入範例：2")
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("0～500", message):
        message = TextSendMessage(text="那是幾個人要一起享用呢？\n輸入範例：2")
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("2", message):
        '''reply_arr=[]
        reply_arr.append(TextSendMessage(text = "沈翔，這邊推薦的食譜如上呦～ \n 請支援圖片"))
        reply_arr.append(TextSendMessage(
                            quick_reply=QuickReply(
                                items=[QuickReplyButton(action=MessageAction(label="重新推薦", text="重新推薦"))])))'''
        menu1 = openFile.openMenuJson('啤酒明蝦')
        menu2 = openFile.openMenuJson('紅油抄手')
        menu3 = openFile.openMenuJson('親子丼')
        reply_arr = []
        message = FlexSendMessage(
            alt_text='價錢區間菜單',
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
        message = TextSendMessage(text='沈翔，這邊推薦的食譜如上呦~',
                                  quick_reply=QuickReply(
                                      items=[QuickReplyButton(action=MessageAction(label="重新推薦", text="重新推薦"))]))
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("好康嚴選", message):
        reply_arr = []
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
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("更多功能", message):
        message = TextSendMessage(text="沈翔，你遇到什麼問題了嗎？",
                                  quick_reply=QuickReply(
                                      items=[
                                            QuickReplyButton(
                                              action=MessageAction(label="新手教學", text="新手教學")),
                                            QuickReplyButton(
                                              action=URIAction(label="設定厭世食材",uri='https://liff.line.me/1656748829-9amYlYbd')),
                                            QuickReplyButton(
                                              action=MessageAction(label="更改地區", text="更改地區")),
                                            QuickReplyButton(
                                              action=MessageAction(label="Q&A", text="Q&A"))]))
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("重新推薦：杏鮑菇",message):
        reply_arr = []
        menu1 = openFile.openMenuJson('炸杏鮑菇')
        menu2 = openFile.openMenuJson('金砂杏鲍菇')
        menu3 = openFile.openMenuJson('龍鬚杏鮑菇')
        menu4 = openFile.openMenuJson('咖哩杏鮑菇炒肉末')
        menu5 = openFile.openMenuJson('氣炸杏鮑菇蔬菜')
        message = FlexSendMessage(
            alt_text='幫我想菜單',
            contents={
                "type": "carousel",
                "contents": [
                    menu1,
                    menu2,
                    menu3,
                    menu4,
                    menu5
                ]
            }  # json貼在這裡
        )
        reply_arr.append(message)
        message = TextSendMessage(text='沈翔，這邊重新推薦的食譜如上呦~',
                                  quick_reply=QuickReply(
                                      items=[QuickReplyButton(action=MessageAction(label="重新推薦", text="重新推薦：杏鮑菇"))]))
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("重新推薦",message):
        reply_arr = []
        menu1 = openFile.openMenuJson('偽韓式台味部隊鍋')
        menu2 = openFile.openMenuJson('可樂雞腿')
        menu3 = openFile.openMenuJson('糖醋脆皮茄子')
        menu4 = openFile.openMenuJson('15分鐘簡易法式吐司')
        menu5 = openFile.openMenuJson('冰花煎餃')
        message = FlexSendMessage(
            alt_text='幫我想菜單',
            contents={
                "type": "carousel",
                "contents": [
                    menu1,
                    menu2,
                    menu3,
                    menu4,
                    menu5
                ]
            }  # json貼在這裡
        )
        reply_arr.append(message)
        message = TextSendMessage(text='沈翔，這邊重新推薦的食譜如上呦~',
                                  quick_reply=QuickReply(
                                      items=[QuickReplyButton(action=MessageAction(label="重新推薦", text="重新推薦"))]))
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("新手教學",message):
        message = TextSendMessage("尚未開放")
        line_bot_api.reply_message(event.reply_token, message)
    elif re.match("更改地區",message):
        message = TextSendMessage("請問沈翔想要查詢北、中、南哪個地區的食材價格呢？",
                                    quick_reply=QuickReply(
                                        items=[
                                            QuickReplyButton(
                                                action=MessageAction(label="北部", text="北部")),
                                            QuickReplyButton(
                                                action=MessageAction(label="中部", text="中部")),
                                            QuickReplyButton(
                                                action=MessageAction(label="南部", text="南部"))]))
        line_bot_api.reply_message(event.reply_token, message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))


# Follow event
@ handler.add(FollowEvent)
def handle_follow(event):
    '''
    # app.logger.info("Got Follow event:" + event.source.user_id)
    buttons_template_message = TemplateSendMessage(
        alt_text='使用政策同意書',
        template=ButtonsTemplate(
            text='阿鼠重視每一個使用者所享有的服務，特此說明使用政策，以保障您的權益。',
            actions=[
                MessageAction(
                    label='查看使用政策說明',
                    text='查看使用政策說明'
                ),
                MessageAction(
                    label='我接受殺必鼠使用政策',
                    text='我接受殺必鼠使用政策'
                )
            ]
        )
    )'''
    '''profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_Name'''
    reply_arr = []
    reply_arr.append(TextSendMessage(text="Hi！沈翔\n歡迎加入『殺必鼠－智慧食價食材』\n我是您最好的機器人夥伴🤖『阿鼠－殺必鼠』🐭🐭\n每天都將提供您市場最新的菜價優惠\n不只如此，還能為您訂做一系列的菜單\n\n自從殺必鼠本人知道最新菜價後\n去菜市場買菜都不會被老闆哄抬價格\n從原本的月底「吃土」改成「吃菜」過生活\n殺必鼠本人用過就回不去了\n真心推薦"))
    reply_arr.append(TextSendMessage(text="請問沈翔想要查詢北、中、南哪個地區的食材價格呢？",
                                        quick_reply=QuickReply(
                                        items=[
                                            QuickReplyButton(
                                                action=MessageAction(label="北部", text="北部")),
                                            QuickReplyButton(
                                                action=MessageAction(label="中部", text="中部")),
                                            QuickReplyButton(
                                                action=MessageAction(label="南部", text="南部"))])))
    #reply_arr.append(buttons_template_message)

    line_bot_api.reply_message(event.reply_token, reply_arr)


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
