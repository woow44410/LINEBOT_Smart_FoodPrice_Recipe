import os
from PIL import ImageFont, ImageDraw,Image
import datetime
import searchSQL
import random
import matplotlib.pyplot as plt
import math

def arrowedLine(im, ptA, ptB, width=1, color=(255,255,255)):
    """Draw line from ptA to ptB with arrowhead at ptB"""
    # Get drawing context
    draw = ImageDraw.Draw(im)
    # # Draw the line without arrows
    # draw.line((ptA,ptB), width=width, fill=color)
    
    x1, y1 = ptA
    x2, y2 = ptB

    xb = 0.85*(x2-x1)+x1
    yb = 0.85*(y2-y1)+y1

    # Work out the other two vertices of the triangle
    # Check if line is vertical
    if x1==x2:
       vtx0 = (xb-10, yb)
       vtx1 = (xb+10, yb)
    # Check if line is horizontal
    elif y1==y2:
       vtx0 = (xb, yb+10)
       vtx1 = (xb, yb-10)
    else:
       alpha = math.atan2(y2-y1,x2-x1)-90*math.pi/180
       print(alpha)
       a = 15*math.cos(alpha)
       b = 15*math.sin(alpha)
       vtx0 = (xb+a, yb+b)
       vtx1 = (xb-a, yb-b)

    #draw.point((xb,yb), fill=(255,0,0))    # DEBUG: draw point of base in red - comment out draw.polygon() below if using this line
    #im.save('DEBUG-base.png')              # DEBUG: save

    # Now draw the arrowhead triangle
    draw.polygon([vtx0, vtx1, ptB], fill=color)
    

# mainFunction
def getIngredientReportPNG(ingreID,ingreName,userID):
    #print("安安",os.path.dirname(os.path.abspath(__file__)))
    resultList = searchSQL.SQL_getIngrePriceByName(ingreName,userID)
    quantityList = searchSQL.SQL_getSeansonAndOutSeansonQuantity(userID,ingreID)

    if resultList[0][0] == None:
        return False

    prePrice = resultList[0][5]
    resultList.reverse()
    id = resultList[0][0]
    name = resultList[0][2]
    avgPriceList = []

    dateList  = []
    for resultTuple in resultList:
        avgPriceList.append(resultTuple[4])
        dateList .append(resultTuple[6])
    
    if quantityList[0][0] != None:
        persentQuantity = (quantityList[0][1]-quantityList[0][0])/quantityList[0][0]
    else:
        persentQuantity = 0

    # 給長條圖用的變數
    pricePercentageList =[]
    for avgPrice in avgPriceList: 
        pricePercentageList.append(round(avgPrice/sum(avgPriceList),2))
    print(avgPriceList)
    
    if max(pricePercentageList) - min(pricePercentageList) > 0.3:
        weight = 2
    elif max(pricePercentageList) - min(pricePercentageList) > 0.2 :
        weight = 3
    elif max(pricePercentageList) - min(pricePercentageList) > 0.1:
        weight = 4
    elif max(pricePercentageList) - min(pricePercentageList) <= 0.1:
        weight = 5
    else:
        weight = 0.5

    # 給漲跌幅用的變數
    ratePriceUpperOrLower = round((avgPriceList[-1]-avgPriceList[-2])/avgPriceList[-2],2)

    # 設定背景圖片與食材圖片
    bkDirPath = os.path.dirname(os.path.abspath(__file__)) + '/image/ingreBackground.png'
    starDirPath = os.path.dirname(os.path.abspath(__file__)) + '/image/star.png'
    ingreDirPath = os.path.dirname(os.path.abspath(__file__)) + f'/ingredient_picture/{id}.jpg'
    
    bk_img = Image.open(bkDirPath).convert('RGBA')
    star_img = Image.open(starDirPath).resize((60,60)).convert('RGBA')

    ingre_img = Image.open(ingreDirPath).resize((250,200)).convert('RGBA')

    # 設置 需要顯示的字體路徑
    fontPath = os.path.dirname(os.path.abspath(__file__)) + "/font/NotoSansTC-Medium.otf"
    # 設置 字體樣式與大小
    font = ImageFont.truetype(fontPath,45)
    fontYear = ImageFont.truetype(fontPath,30)
    fontPrice = ImageFont.truetype(fontPath,25)
    # 設置 讓圖片可以被拿來壞壞
    draw = ImageDraw.Draw(bk_img)

    ## 繪製上半部
    draw.text((400,20),"今日估計價格：{:.1f} 元/臺斤".format(prePrice),font=font,fill=(0,123,37))
    # 繪製漲/幅
    draw.text((400,90),f"漲 / 跌幅：{ratePriceUpperOrLower}%",font=font,fill=(0,123,37))
    # 繪製推薦指數
    draw.text((400,160),"推薦指數：",font=font,fill=(0,123,37))

    ## 繪製下半部
    # 繪製食材名稱
    draw.text((40,270),f"{name}",font=font,fill=(255,255,255))
    # 繪製今年
    year = datetime.datetime.now().date().strftime("%Y")
    draw.text((40,340),f"{year}",font=fontYear,fill=(255,255,255))
    # 繪製是不是產季
    if persentQuantity > 0.6:
        draw.text((850,270),"產季",font=font,fill=(255,255,255))
    else:
        draw.text((850,270),"非產季",font=font,fill=(255,255,255))

    # 繪製長條圖 x1,y1,x2,y2 其中y2變動會影響高低,x1只是位置 fill是顏色
    # y最高450 最低800 左上角座標(0,0)
    recXAxis = 0
    # 紀錄上個長條圖的位置 方便畫線
    preX2Axis = 0
    preY2Axis = 0
    # 紀錄上個價格
    preAvgPrice = 0
    print(weight)
    for i,price in enumerate(pricePercentageList):
        # 定義長條圖的左下角跟右上角
        x1 = 90+recXAxis
        y1 = 900
        x2 = 125+recXAxis
        y2 = 900-(450*price*weight)
        draw.rectangle((x1,y1,x2, y2),fill=(251,181,64))
        # 價格要塞在左右長條圖的中間
        avgXAxis = (preX2Axis + x2-100 )/2
        avgYAxis = (preY2Axis + y2-100 )/2
        tmpAvgPrice = 0
        if i != 0:
            tmpAvgPrice = avgPriceList[i] - preAvgPrice
            if avgPriceList[i] - preAvgPrice >=0:
                # print("安安")
                # print(x2-50)
                # print(preX2Axis)
                # print(y2-10)
                # print(preY2Axis,"\n")
                draw.line((preX2Axis,preY2Axis,x2-50,y2-10),fill=(255,255,255),width=7)
                if y2-10 == preY2Axis:
                    arrowedLine(bk_img,(preX2Axis,preY2Axis),(x2-40,y2-10))
                    draw.text((avgXAxis-10,avgYAxis-10 ),"{:<5.2f}元".format(tmpAvgPrice),font = fontPrice,fill=(255,255,255))
                else:
                    arrowedLine(bk_img,(preX2Axis,preY2Axis),(x2-40,y2-17))
                    draw.text((avgXAxis-10,avgYAxis-10 ),"{:<5.2f}元".format(tmpAvgPrice),font = fontPrice,fill=(255,255,255))
                
            else:
                draw.line((preX2Axis,preY2Axis,x2-50,y2-10),fill=(255,67,55),width=7)
                if y2-10 == preY2Axis:
                    arrowedLine(bk_img,(preX2Axis,preY2Axis),(x2-40,y2-10),color=(255,67,55))
                    draw.text((avgXAxis+7,avgYAxis-7),"{:<5.2f}元".format(tmpAvgPrice),font = fontPrice,fill=(255,67,55))
                else:
                    arrowedLine(bk_img,(preX2Axis,preY2Axis),(x2-40,y2-5),color=(255,67,55))
                    draw.text((avgXAxis+16,avgYAxis-7),"{:<5.2f}元".format(tmpAvgPrice),font = fontPrice,fill=(255,67,55))
        
        preX2Axis = x2 +5
        preY2Axis = y2 -10
        preAvgPrice = avgPriceList[i]

        #draw.text((85+recXAxis,900-(450*price*weight)-40 ),"{:.1f}".format(avgPriceList[i]),font = fontPrice,fill=(255,255,255))
        recXAxis = recXAxis + 135

    # 繪製下面那個直線
    draw.line((70,900,970,900),fill=(255,255,255),width=5)

    

    # 繪製日期
    dateXAxis = 0
    for date in dateList:
        date =  date.split(".",1)[1].replace(".","/")
        draw.text((70+dateXAxis,910),f"{date}",font=fontYear,fill=(255,255,255))
        dateXAxis = dateXAxis + 135

    # # 繪製食譜名稱1
    # draw.text((160,905),"食譜1",font=font,fill=(255,255,255))

    # # 繪製食譜名稱2
    # draw.text((455,905),"食譜2",font=font,fill=(255,255,255))

    # # 繪製食譜名稱3
    # draw.text((750,905),"食譜3",font=font,fill=(255,255,255))

    # 把食材圖片沾黏上去
    tmpStar = 1
    if persentQuantity > -0.3:
        tmpStar += 1
    if persentQuantity > 0:
        tmpStar += 1
    if persentQuantity > 0.3:
        tmpStar += 1
    if persentQuantity > 0.6:
        tmpStar += 1
    xAxis = 80
    for i in range(tmpStar):
        bk_img.paste(star_img,(630+xAxis*i,160),mask=star_img.split()[3])
    # bk_img.paste(star_img,(710,160),mask=star_img.split()[3])
    # bk_img.paste(star_img,(790,160),mask=star_img.split()[3])
    # bk_img.paste(star_img,(870,160),mask=star_img.split()[3])

    bk_img.paste(ingre_img,(50,30),mask=None)

    responseDirPath = os.path.dirname(os.path.abspath(__file__))+f'/response_LineBot/menuBtn1/{id}.png'
    bk_img.save(responseDirPath,"PNG")
    
    randomNumber = random.randint(1,100000) 
    return f'https://misIntro.asuscomm.com:5001/ingredient/richMenu/{id}.png#?random={randomNumber}'
    # # 展示出我X媽花六個小時畫的圖片
    #bk_img.show()
