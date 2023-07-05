import connectMSSQL
import hashlib
from linebot import (
    LineBotApi, WebhookHandler
)

# 透過userID取得userName
def getUserName(userID):
    try:
        # 必須放上自己的Channel Access Token
        line_bot_api = LineBotApi('snfd0pJkVVClMxOZECyIAEVe967tFFD0B7vSQhfy4o8mNxl5K6yF5EG31+kKYiEvqYxWPRnzBqFKGBcForbU6PR51Vc7hJ2neyYE9/b36BRZ/QAFJ+22Zj2+FNn6TBi+duDI7i5ODCYZlcuQB5d//wdB04t89/1O/w1cDnyilFU=')
        profile = line_bot_api.get_profile(userID)
        userName = profile.display_name
        return userName
    except:
        print("userID:{} 錯誤!!".format(userID))
        return 'None'

# 查看User有沒有在資料庫
# 有的話更新Name 沒有的話插入ID和Name
def SQL_checkUserExists(userID,userName):
    try:
        # print(f"EXEC dbo.checkUserExists @inputID='{userID}' ,@inputName='{userName}'")
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.checkUserExists @inputID='{userID}' ,@inputName='{userName}'")
        cursor.close()
    except:
        print("查詢使用者錯誤")

# 給Liff用於抓取資料
def SQL_getIngredientAll(userID = 'None'):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.getIngredientAll @inputID='{userID}'")
        result = cursor.fetchall()
        cursor.close()
        return result
    except:
        print("查詢使用者錯誤")

# 正當管道 就會有token可以生
def SQL_createLiffToken(userID):
    try:
        token = hashlib.md5()
        token.update(userID.encode(encoding='utf-8'))
        token = token.hexdigest()

        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.createLiffToken @inputID='{userID}',@inputToken='{token}'")
        cursor.close()
        return token
    except:
        print("查詢使用者錯誤")

# 刪除使用者之前不喜歡的菜
def SQL_checkLiffToken(userID,token='None'):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.checkLiffToken @inputID='{userID}'")
        result = cursor.fetchall()
        if token == result[0][0]:
            #print(f"userID:{userID},token驗證成功")
            # 將原本的不喜歡食材刪除
            cursor.execute(f"EXEC dbo.deleteOriUnlikeIngre @inputID='{userID}'")
            cursor.close()
            return True
        else:
            #print(f"userID:{userID},token驗證失敗")
            cursor.close()
            return False
    except:
        print(f"userID:{userID},SQL_checkLiffToken出錯")

# 插入使用者不喜歡的菜
def SQL_insertNewUnlikeIngr(values):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"insert into user_unlike_ingredient (user_id,ingredient_id)\
            values {values}")
        cursor.close()
        return True
    except:
        print("查詢使用者錯誤")

# 得到全部蔬菜和水果的ID 用於爬蟲
def SQL_getIngreVegeAndFruit():
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute("EXEC dbo.getIngreVegeAndFruitID")
        result = cursor.fetchall()
        cursor.close()
        return result
    except:
        print("查詢蔬菜和水果ID錯誤")

# 得到全部海鮮ID 用於爬蟲
def SQL_getIngreSeaFoodID():
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute("EXEC dbo.getIngreSeaFoodID")
        result = cursor.fetchall()
        cursor.close()
        return result
    except:
        print("查詢蔬菜和水果ID錯誤")

# 將爬蟲得到的價格插入 ingredient_price資料表中
def SQL_insertIngredientPrice(value):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"insert into ingredient_price\
            (date,id,market_name,upper_price,middle_price,lower_price,avg_price,trans_quantity)\
                values {value}")
        cursor.close()
        print("插入價格成功")
        return True
    except:
        print("插入價格錯誤")
        return False

# 找出擁有相同commName的ingreID
def SQL_getIngreSameCommNameID(ingreCommName):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.getIngreSameCommnameID @inputName='{ingreCommName}'")
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as ex :
        print(ex)

# 透過學名和市場名稱找到食材的7天價格
def SQL_getIngrePriceByName(ingreName,userID):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.getIngrePriceByName \
            @inputName='{ingreName}', @inputID='{userID}'")
        result = cursor.fetchall()
        #print(result)
        cursor.close()
        print("成功!!找到價格了好耶")
        return result
    except:
        print("哭阿QQ 找不到阿")
        return False

# 更新user的狀態
def SQL_updateUserStatus(userID,statusID):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.updateUserStatus \
            @inputID='{userID}', @inputStatusID='{statusID}' ")
        cursor.close()
        print(f"userID = {userID},使用者狀態更新成功")
        return True
    except:
        print(f"userID = {userID},使用者狀態更新失敗")
        return False

# 更新user的地區
def SQL_updateUserMarketName(userID,marketName):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.updateUserMarketName\
            @inputID='{userID}', @inputMarketName='{marketName}' ")
        cursor.close()
        print(f"userID = {userID},使用者地區更新成功")
        return True
    except:
        print(f"userID = {userID},使用者地區更新失敗")
        return False

# 取得user目前的狀態
def SQL_getUserStatusAndMarketName(userID):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.getUserStatusAndMarketName @inputID='{userID}'")
        result = cursor.fetchall()
        cursor.close()
        print(f"userID = {userID},取得使用者狀態成功")
        return result
    except:
        print(f"userID = {userID},使用者狀態更新失敗")
        return False

# 看食譜有沒有存在於資料庫 有的話就更新 沒有的話就插入
def SQL_checkRecipeExists(id,name,imgUrl,portion,time,calorie,recipeUrl):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.checkRecipeExists\
            @inputID='{id}', @inputName='{name}',\
            @inputImgUrl='{imgUrl}', @inputPortion='{portion}',\
            @inputTime='{time}', @inputCalorie='{calorie}', \
            @inputRecipeUrl='{recipeUrl}' ")
        cursor.close()
        print(f"recipeID = {id},更新食譜成功")
        return True
    except:
        print(f"recipeID = {id},更新食譜失敗")
        return False

# 更新食譜裡面的食材
def SQL_deleteAndInsertRecipeIngredients(id,value):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"delete from recipe_ingredient \
            where recipe_ingredient.id ='{id}'")
        cursor.execute(f"insert into recipe_ingredient values {value}")
        cursor.close()
        #print(f"recipeID = {id},食譜內容更新成功")
    except:
        print(f"recipeID = {id},食譜內容更新失敗")

# 自動幫使用生成食譜，排除不喜歡的食材
def SQL_getRandomRecipeWithOutCommName(inputUserID):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.getRandomRecipeWithOutCommName @inputUserID= '{inputUserID}'")
        #cursor.execute(f"select a.id,a.name,a.img_url,a.portion,a.time,a.calorie,a.recipe_url, b.ingredient_name,b.ingredient_quantity from recipe_ingredient b right join (select top 7 id, name, img_url, portion, time, calorie, recipe_url from recipe order by NEWID()) a on a.id = b.id where a.name like + '%'+ {commName} +'%'")
        result = cursor.fetchall()
        cursor.close()
        print(f"userID = {inputUserID},抓取食譜成功")
        return result
    except:
        print(f"userID = {inputUserID},抓取食譜失敗")

# 透過食材名稱得到7筆食譜
def SQL_getRandomRecipeByCommName(userID,commName):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.getRandomRecipeByCommName @inputUserID='{userID}', @inputCommName= '{commName}'")
        #cursor.execute(f"select a.id,a.name,a.img_url,a.portion,a.time,a.calorie,a.recipe_url, b.ingredient_name,b.ingredient_quantity from recipe_ingredient b right join (select top 7 id, name, img_url, portion, time, calorie, recipe_url from recipe order by NEWID()) a on a.id = b.id where a.name like + '%'+ {commName} +'%'")
        result = cursor.fetchall()
        cursor.close()
        print(f"recipeName = {commName},抓取食譜成功")
        return result
    except:
        print(f"recipeName = {commName},抓取食譜失敗")

# 透過輸入人數的到相對應的食譜，一樣會把不喜歡的弄掉
def SQL_getRandomRecipeByPortion(inputUserID,portion):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.getRandomRecipeByPortion \
            @inputUserID='{inputUserID}', @inputPortion= '{portion}'")
        #cursor.execute(f"select a.id,a.name,a.img_url,a.portion,a.time,a.calorie,a.recipe_url, b.ingredient_name,b.ingredient_quantity from recipe_ingredient b right join (select top 7 id, name, img_url, portion, time, calorie, recipe_url from recipe order by NEWID()) a on a.id = b.id where a.name like + '%'+ {commName} +'%'")
        result = cursor.fetchall()
        cursor.close()
        print(f"recipePortion = {portion},抓取Portion成功")
        return result
    except:
        print(f"recipePortion = {portion},抓取Portion失敗")

# 透過輸入人數的到相對應的食譜，一樣會把不喜歡的弄掉
def SQL_getSeansonAndOutSeansonQuantity(inputUserID,inputIngredientID):
    try:
        cursor = connectMSSQL.connectMsSQL()
        cursor.execute(f"EXEC dbo.getSeansonAndOutSeansonQuantity \
            @inputUserID='{inputUserID}', @inputIngredientID= '{inputIngredientID}'")
        #cursor.execute(f"select a.id,a.name,a.img_url,a.portion,a.time,a.calorie,a.recipe_url, b.ingredient_name,b.ingredient_quantity from recipe_ingredient b right join (select top 7 id, name, img_url, portion, time, calorie, recipe_url from recipe order by NEWID()) a on a.id = b.id where a.name like + '%'+ {commName} +'%'")
        result = cursor.fetchall()
        cursor.close()
        print(f"抓取inpuIngredientID:{inputIngredientID}產量成功")
        return result
    except:
        print(f"抓取inpuIngredientID:{inputIngredientID}產量失敗")