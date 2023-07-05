import crower
import json
import re
import emoji
import searchSQL
import time
import richMenu2


def getMenuListJsonByName(inputUserID,inputName):
    try:
        
        resultList = searchSQL.SQL_getRandomRecipeByCommName(inputUserID,inputName)
        # for i in resultList:
        #     print(i)
        if len(resultList) == 0:
            for i in range(1,3):
                crowerResult = crower.crower(inputName,i)
                print("成功")
                richMenu2.updateRecipeTwoTable(crowerResult)
            return "請稍後正在爬蟲中"
        #print(len(resultList))
        
        recipeJsonList =  richMenu2.getRecipeJsonList(resultList)
        return recipeJsonList
    except:
        print(f"error:getMenuLsitJsonByName({inputName})")
