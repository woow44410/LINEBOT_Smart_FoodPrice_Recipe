import os
from PIL import ImageFont, ImageDraw,Image
import datetime

def getIngredientReportPNG():
    ## ref
    # id,name,avgPriceList,prePrice,dateList

    # 暫存專區
    id = 'LA1'
    name = '甘藍-初秋'
    avgPriceList = [33.2,43.4,42,38.1,34.3,36.3,37.5]
    prePrice = 49.8
    dateList = ['110.12.21','110.12.19','110.12.18','110.12.17','110.12.16','110.12.15','110.12.14']

    # 給長條圖用的變數
    pricePercentageList =[]
    for avgPrice in avgPriceList: 
        pricePercentageList.append(round(avgPrice/sum(avgPriceList),2))

    # 給漲跌幅用的變數
    ratePriceUpperOrLower = round((avgPriceList[-1]-avgPriceList[-2])/avgPriceList[-2],2)

    # 設定背景圖片與食材圖片
    bkDirPath = os.path.dirname(__file__) + '/image/ingreBackground.png'
    ingreDirPath = os.path.dirname(__file__) + f'/ingredient_picture/{id}.jpg'
    bk_img = Image.open(bkDirPath)
    ingre_img = Image.open(ingreDirPath).resize((250,200))

    # 設置 需要顯示的字體路徑
    fontPath = os.path.dirname(__file__) + "/font/NotoSansTC-Medium.otf"
    # 設置 字體樣式與大小
    font = ImageFont.truetype(fontPath,45)
    fontYear = ImageFont.truetype(fontPath,30)
    fontPrice = ImageFont.truetype(fontPath,25)
    # 設置 讓圖片可以被拿來壞壞
    draw = ImageDraw.Draw(bk_img)

    ## 繪製上半部
    draw.text((400,30),f"今日估計價格：{prePrice}元/臺斤",font=font,fill=(0,123,37))
    # 繪製漲/幅
    draw.text((400,100),f"漲 / 跌幅：{ratePriceUpperOrLower}%",font=font,fill=(0,123,37))
    # 繪製推薦指數
    draw.text((400,170),"推薦指數：兩星",font=font,fill=(0,123,37))

    ## 繪製下半部
    # 繪製食材名稱
    draw.text((40,270),f"{name}",font=font,fill=(255,255,255))
    # 繪製今年
    year = datetime.datetime.now().date().strftime("%Y")
    draw.text((40,340),f"{year}",font=fontYear,fill=(255,255,255))
    # 繪製是不是產季
    draw.text((850,270),"產季",font=font,fill=(255,255,255))

    # 繪製長條圖 x1,y1,x2,y2 其中y2變動會影響高低,x1只是位置 fill是顏色
    # y最高450 最低800 左上角座標(0,0)
    recXAxis = 0
    for i,price in enumerate(pricePercentageList):
        draw.rectangle((105+recXAxis, 800, 135+recXAxis, 800-(350*price*6) ),fill=(251,181,64))
        draw.text((95+recXAxis,800-(350*price*6)-40 ),"{:.1f}".format(avgPriceList[i]),font = fontPrice,fill=(255,255,255))
        recXAxis = recXAxis + 135

    # 繪製下面那個直線
    draw.line((80,800,980,800),fill=(255,255,255),width=5)

    # 繪製日期
    dateXAxis = 0
    for date in dateList:
        date =  date.split(".",1)[1].replace(".","/")
        draw.text((80+dateXAxis,810),f"{date}",font=fontYear,fill=(255,255,255))
        dateXAxis = dateXAxis + 135

    # 繪製食譜名稱1
    draw.text((160,915),"食譜1",font=font,fill=(255,255,255))

    # 繪製食譜名稱2
    draw.text((460,915),"食譜2",font=font,fill=(255,255,255))

    # 繪製食譜名稱3
    draw.text((760,915),"食譜3",font=font,fill=(255,255,255))

    # 把食材圖片沾黏上去
    bk_img.paste(ingre_img,(50,40),mask=None)

    # 展示出我X媽花六個小時畫的圖片
    bk_img.show()
getIngredientReportPNG()