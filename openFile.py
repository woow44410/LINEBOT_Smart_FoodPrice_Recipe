import json
import os

def openIngredientAllKinds():
    text = []
    text.append(openVegeAllKinds())
    text.append(openFruitAllKinds())
    text.append(openMealAllKinds())
    text.append(openFishAllKinds())
    text.append(openBeanAllKinds())
    return text

def openVegeAllKinds():
    dirPath = os.path.dirname(os.path.abspath(__file__))+'/foods/01_vegetables/蔬菜分類(代號-名稱-俗名).json'
    with open(dirPath,'r',encoding='utf-8') as fp:
        text = json.load(fp)
        fp.close()
    return text

def openFruitAllKinds():
    dirPath = os.path.dirname(os.path.abspath(__file__))+'/foods/02_fruits/水果分類(代號-名稱-俗名).json'
    with open(dirPath,'r',encoding='utf-8') as fp:
        text = json.load(fp)
        fp.close()
    return text

def openMealAllKinds():
    dirPath = os.path.dirname(os.path.abspath(__file__))+'/foods/03_meals/肉分類(代號-名稱-俗名).json'
    with open(dirPath,'r',encoding='utf-8') as fp:
        text = json.load(fp)
        fp.close()
    return text

def openFishAllKinds():
    dirPath = os.path.dirname(os.path.abspath(__file__))+'/foods/04_fishes/魚分類(代號-名稱-俗名).json'
    with open(dirPath,'r',encoding='utf-8') as fp:
        text = json.load(fp)
        fp.close()
    return text

def openBeanAllKinds():
    dirPath = os.path.dirname(os.path.abspath(__file__))+'/foods/05_beans/豆分類(代號-名稱-俗名).json'
    with open(dirPath,'r',encoding='utf-8') as fp:
        text = json.load(fp)
        fp.close()
    return text

def openMenuJson(fileName):
    dirPath = os.path.dirname(os.path.abspath(__file__))+'/menu_json_v2/'+fileName+'.json'
    with open(dirPath,'r',encoding='utf-8') as fp:
        text = json.load(fp)
        fp.close()
    return text
