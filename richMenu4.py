import searchSQL
import richMenu2


def getMenuListJsonByPortion(userID,inputName):
    resultList = searchSQL.SQL_getRandomRecipeByPortion(userID,inputName)
    recipeJsonList = richMenu2.getRecipeJsonList(resultList)
    return recipeJsonList

