import crower
import json
import re
import emoji
import searchSQL
import time



def getMenuListJsonByUserID(userID):
    try:
        resultList = searchSQL.SQL_getRandomRecipeWithOutCommName(userID)
        recipeJsonList =  getRecipeJsonList(resultList)
        return recipeJsonList
    except:
        print(f"error:getMenuLsitJsonByName({userID})")


def updateRecipeTwoTable(recipeList):
    for i,recipe in enumerate(recipeList):
        value1 = []
        id = recipe['id'] if recipe['id']==None else strip_emoji(recipe['id'])
        name = recipe['name'] if recipe['name']==None else strip_emoji(recipe['name'])
        imgUrl = recipe['img'] if recipe['img']==None else strip_emoji(recipe['img'])
        portion = recipe['portion'] if recipe['portion']==None else strip_emoji(recipe['portion'])
        time = recipe['time'] if recipe['time']==None else strip_emoji(recipe['time'])
        calorie = recipe['calorie'] if recipe['calorie']==None else strip_emoji(recipe['calorie'])
        recipeUrl = recipe['url'] if recipe['url']==None else strip_emoji(recipe['url'])
        print(imgUrl)
        searchSQL.SQL_checkRecipeExists(id,name,imgUrl,portion,time,calorie,recipeUrl)

        value2 = []
        tupleValue = []
        try:
            for ingredient in recipe["Ingredients"]:
                value2.append(id)
                value2.append(ingredient[0].replace(","," "))
                value2.append(ingredient[1].replace(","," "))
                tupleValue.append(tuple(value2))
                value2= []
            tupleValue = "('" + str(tupleValue).split("[('",1)[1].split("')]",1)[0] + "')"
            searchSQL.SQL_deleteAndInsertRecipeIngredients(id,tupleValue)
        except:
            print(f"目前第{i+1}筆,recipeID={id},更新失敗")


def strip_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    new_text = new_text.replace(","," ")
    new_text = new_text.replace(" ","")
    return new_text

def getRecipeJsonList(resultList):
    id = "0"
    recipeList = []
    tmp  = 1
    ingredientNameList = []
    ingredientQuantityList = []
    # print(resultList)
    for result in resultList:
        
        # print(result)
        if id != result[0]:
            # print(id)
            id = result[0]
            name = result[1]
            imgUrl = result[2]
            portion = result[3]
            cookTime = result[4]
            calorie = "阿災" if result[5] == None else result[5]
            recipeUrl = result[6]
            if tmp == 0:
                # print(id,name,imgUrl,portion,cookTime,calorie,recipeUrl,ingredientNameList,ingredientQuantityList)
                recipeJson = createRecipeJson(name,imgUrl,portion,cookTime,calorie,recipeUrl,ingredientNameList,ingredientQuantityList)
                recipeList.append(recipeJson)
                ingredientNameList = []
                ingredientQuantityList = []
            else:
                tmp = 0
        ingredientNameList.append(result[7])
        ingredientQuantityList.append(result[8])
    return recipeList

# 生成食譜json 
def createRecipeJson(name,imgUrl,portion,cookTime,calorie,recipeUrl,ingreNameList,ingreQuantityList):
    # name = "親子丼"
    # imgUrl = "https://i.imgur.com/zKORoI3.jpg"
    # recipeUrl = "https://icook.tw/recipes/392920"
    # ingreNameList = ["鹽巴","蒜頭"]
    # ingreQuantityList = ["少許","一顆"]
    # calorie = "540"
    # portion = "4"
    # cookTime = "20"
    tipsList = [calorie+"大卡",portion+"人份",cookTime+"分鐘"]
    tipsNameList = ["熱量","份量","時間"]

    response = {}
    response["type"] = "bubble"

    response["hero"] = {}
    response["hero"]["type"] = "image"
    response["hero"]["url"]= f"{imgUrl}"
    response["hero"]["size"] = "full"
    response["hero"]["aspectMode"] = "cover"
    response["hero"]["action"] = {}
    response["hero"]["action"]["type"]= "uri"
    response["hero"]["action"]["label"] = "action"
    response["hero"]["action"]["uri"] = f"{recipeUrl}"
    response["hero"]["action"]["altUri"] = {}
    response["hero"]["action"]["altUri"]["desktop"] = f"{recipeUrl}"
    response["hero"]["aspectRatio"] = "20:13"

    response["body"] = {}
    response["body"]["type"] = "box"
    response["body"]["layout"] = "vertical"
    response["body"]["contents"] = []
    response["body"]["contents"].append({})
    response["body"]["contents"][0]["type"] = "text"
    response["body"]["contents"][0]["text"] = f"{name}"
    response["body"]["contents"][0]["weight"] = "bold"
    response["body"]["contents"][0]["color"] = "#000000"
    response["body"]["contents"][0]["size"] = "xl"
    response["body"]["contents"].append({})
    response["body"]["contents"][1]["type"] = "box"
    response["body"]["contents"][1]["layout"] = "vertical"
    response["body"]["contents"][1]["margin"] = "xxl"
    response["body"]["contents"][1]["spacing"] = "sm"
    response["body"]["contents"][1]["contents"] = []
    tmp = 0
    for i,(ingreName,ingreQuantity) in enumerate(zip(ingreNameList,ingreQuantityList)):
        
        response["body"]["contents"][1]["contents"].append({})
        response["body"]["contents"][1]["contents"][i]["type"] = "box"
        response["body"]["contents"][1]["contents"][i]["layout"] = "horizontal"
        response["body"]["contents"][1]["contents"][i]["contents"] = []
        response["body"]["contents"][1]["contents"][i]["contents"].append({})
        response["body"]["contents"][1]["contents"][i]["contents"][0]["type"] = "text"
        response["body"]["contents"][1]["contents"][i]["contents"][0]["text"] = ingreName
        response["body"]["contents"][1]["contents"][i]["contents"][0]["size"] = "sm"
        response["body"]["contents"][1]["contents"][i]["contents"][0]["color"] = "#555555"
        response["body"]["contents"][1]["contents"][i]["contents"][0]["flex"] = 0
        response["body"]["contents"][1]["contents"][i]["contents"].append({})
        response["body"]["contents"][1]["contents"][i]["contents"][1]["type"] = "text"
        response["body"]["contents"][1]["contents"][i]["contents"][1]["text"] = ingreQuantity
        response["body"]["contents"][1]["contents"][i]["contents"][1]["size"] = "sm"
        response["body"]["contents"][1]["contents"][i]["contents"][1]["color"] = "#111111"
        response["body"]["contents"][1]["contents"][i]["contents"][1]["align"] = "end"
        tmp = i
    
    
    tmp = tmp +1
    
    response["body"]["contents"][1]["contents"].append({})
    response["body"]["contents"][1]["contents"][tmp]["type"] = "separator"
    response["body"]["contents"][1]["contents"][tmp]["margin"] = "xxl"
    response["body"]["contents"][1]["contents"][tmp]["color"] = "#000000"

    for i,(tipsName,tips) in enumerate(zip(tipsNameList,tipsList)):
        tmp = tmp +1
        # print(i)
        # print(tmp)
        response["body"]["contents"][1]["contents"].append({})
        
        response["body"]["contents"][1]["contents"][tmp]["type"] = "box"
        response["body"]["contents"][1]["contents"][tmp]["layout"] = "horizontal"
        if i == 0:
            response["body"]["contents"][1]["contents"][tmp]["margin"] = "xxl"
        response["body"]["contents"][1]["contents"][tmp]["contents"] = []
        response["body"]["contents"][1]["contents"][tmp]["contents"].append({})
        response["body"]["contents"][1]["contents"][tmp]["contents"][0]["type"] = "text"
        response["body"]["contents"][1]["contents"][tmp]["contents"][0]["text"] = f"{tipsName}："
        response["body"]["contents"][1]["contents"][tmp]["contents"][0]["size"] = "sm"
        response["body"]["contents"][1]["contents"][tmp]["contents"][0]["color"] = "#555555"
        response["body"]["contents"][1]["contents"][tmp]["contents"].append({})
        response["body"]["contents"][1]["contents"][tmp]["contents"][1]["type"] = "text"
        response["body"]["contents"][1]["contents"][tmp]["contents"][1]["text"] = f"{tips}"
        response["body"]["contents"][1]["contents"][tmp]["contents"][1]["size"] = "sm"
        response["body"]["contents"][1]["contents"][tmp]["contents"][1]["color"] = "#111111"
        response["body"]["contents"][1]["contents"][tmp]["contents"][1]["align"] = "end"

    response["styles"] = {}
    response["styles"]["footer"] = {}
    response["styles"]["footer"]["separator"] = True
    
    return response

