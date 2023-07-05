import os
from PIL import ImageFont, ImageDraw,Image

## 版本2
bkDirPath = os.path.dirname(__file__) + '/image/ingreBackground.png'
ingreDirPath = os.path.dirname(__file__) + '/ingredient_picture/11.jpg'

bk_img = Image.open(bkDirPath)
ingre_img = Image.open(ingreDirPath)
ingre_img = ingre_img.resize((250,200))

windowsName = 'My Image'
pre_price = '100'

# 設置需要顯示的字體路徑
fontPath = os.path.dirname(__file__) + "/font/NotoSansTC-Medium.otf"
# 設置字體大小
font = ImageFont.truetype(fontPath,45)
fontYear = ImageFont.truetype(fontPath,30)
# 設置讓圖片可以被寫文字
#img_pil = Image.fromarray(bk_img)
draw = ImageDraw.Draw(bk_img)


# 繪製文字在圖上 ((x,y),text,font,fill = color)
## 上半部
# 繪製今日估計價格
draw.text((400,30),"今日估計價格：78元/臺斤",font=font,fill=(0,123,37))
# 繪製漲/幅
draw.text((400,100),"漲 / 跌幅：+10%",font=font,fill=(0,123,37))
# 繪製推薦指數
draw.text((400,170),"推薦指數：兩星",font=font,fill=(0,123,37))

# 繪製食材名稱
draw.text((40,270),"高麗菜",font=font,fill=(255,255,255))
# 繪製今年
draw.text((40,340),"2021",font=fontYear,fill=(255,255,255))
# 繪製是不是產季
draw.text((850,270),"非產季",font=font,fill=(255,255,255))

## 下半部
# 繪製Day1 長條圖 x1,y1,x2,y2 其中y2變動會影響高低,x1只是位置
draw.rectangle((105,800,135,450),fill=(251,181,64))

# 繪製Day2 長條圖
draw.rectangle((240,800,270,450),fill=(251,181,64))

# 繪製Day3 長條圖
draw.rectangle((375,800,405,450),fill=(251,181,64))

# 繪製Day4 長條圖
draw.rectangle((510,800,540,450),fill=(251,181,64))

# 繪製Day5 長條圖
draw.rectangle((645,800,675,450),fill=(251,181,64))

# 繪製Day6 長條圖
draw.rectangle((780,800,810,450),fill=(251,181,64))

# 繪製Day7 長條圖
draw.rectangle((915,800,945,450),fill=(251,181,64))


# 繪製下面那個直線
draw.line((80,800,980,800),fill=(255,255,255),width=5)

# 繪製Day1 日期 x+=135,y=y
draw.text((80,810),"12/16",font=fontYear,fill=(255,255,255))

# 繪製Day2 日期
draw.text((215,810),"12/17",font=fontYear,fill=(255,255,255))

# 繪製Day3 日期
draw.text((350,810),"12/18",font=fontYear,fill=(255,255,255))

# 繪製Day4 日期
draw.text((485,810),"12/19",font=fontYear,fill=(255,255,255))

# 繪製Day5 日期
draw.text((620,810),"12/20",font=fontYear,fill=(255,255,255))

# 繪製Day6 日期
draw.text((755,810),"12/21",font=fontYear,fill=(255,255,255))

# 繪製Day7 日期
draw.text((890,810),"12/22",font=fontYear,fill=(255,255,255))




# 把食材圖片沾黏上去
bk_img.paste(ingre_img,(50,40),mask=None)
bk_img.show()

# # 調整視窗大小
# cv2.namedWindow(windowsName,0)
# cv2.resizeWindow(windowsName,(700,700))

# # 顯示圖片
# cv2.imshow(windowsName, bk_img)

# # 按下任意鍵則關閉所有視窗
# cv2.waitKey(0)
# cv2.destroyAllWindows()













## 版本1
# bkDirPath = os.path.dirname(__file__) + '/image/ingreBackground.png'
# ingreDirPath = os.path.dirname(__file__) + '/ingredient_picture/11.jpg'

# bk_img = cv2.imread(bkDirPath)
# ingre_img = cv2.imread(bkDirPath)

# windowsName = 'My Image'
# pre_price = '100'

# # 設置需要顯示的字體路徑
# fontPath = os.path.dirname(__file__) + "/font/NotoSansTC-Medium.otf"
# # 設置字體大小
# font = ImageFont.truetype(fontPath,45)
# fontYear = ImageFont.truetype(fontPath,30)
# # 設置讓圖片可以被寫文字
# img_pil = Image.fromarray(bk_img)
# draw = ImageDraw.Draw(img_pil)


# # 繪製文字在圖上 ((x,y),text,font,fill = color)
# # 繪製今日估計價格
# draw.text((400,30),"今日估計價格：78元/臺斤",font=font,fill=(0,123,37))
# # 繪製漲/幅
# draw.text((400,100),"漲 / 跌幅：+10%",font=font,fill=(41,146,75))
# # 繪製推薦指數
# draw.text((400,170),"推薦指數：兩星",font=font,fill=(41,146,75))

# # 繪製食材名稱
# draw.text((40,270),"高麗菜",font=font,fill=(255,255,255))
# # 繪製今年
# draw.text((40,340),"2021",font=fontYear,fill=(255,255,255))
# # 繪製是不是產季
# draw.text((850,270),"非產季",font=font,fill=(255,255,255))

# bk_img = img_pil

# # 調整視窗大小
# cv2.namedWindow(windowsName,0)
# cv2.resizeWindow(windowsName,(700,700))

# # 顯示圖片
# cv2.imshow(windowsName, bk_img)

# # 按下任意鍵則關閉所有視窗
# cv2.waitKey(0)
# cv2.destroyAllWindows()