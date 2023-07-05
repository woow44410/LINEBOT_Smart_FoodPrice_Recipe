import requests
import datetime
import os
import searchSQL
import time

def getIngredientPriceJson():
    startTime,endTime = getEndTimeAndStartTime()
    marketNameList = ['台北一','台中市','高雄市']
    page = 1
    api_key = '7SVJIDBVQPP2HFSK9KDUDJ15V7RE5Q'

    # dirPath = os.path.dirname(os.path.abspath(__file__)) + '/ingredient_price/{}2.json'
    url = "https://data.coa.gov.tw/api/v1/AgriProductsTransType/?Start_time={}&End_time={}&MarketName={}&Page={}&api_key={}"
    
    # 取得cropCode的清單
    resultList = searchSQL.SQL_getIngreVegeAndFruit()
    cropCodeList = []
    for i in range(len(resultList)):
        cropCodeList.append(resultList[i][0])

    print(cropCodeList)
    returnList = []
    for marketName in marketNameList:
        while True:
            uri = url.format(startTime,endTime,marketName,page,api_key)
            response = requests.get(uri).json()
            print(f"目前在{marketName},第{page}筆")
            # 代表這頁沒東西
            if len(response['Data']) == 0:
                page = 1
                break
            # 代表這頁好像有點東西
            else:
                for i , cropCode in enumerate(cropCodeList):
                    for data in response['Data']:
                        # print(data['CropCode'])
                        if cropCode == data['CropCode']:
                            data.pop("CropName")
                            data.pop("MarketCode")
                            returnList.append(tuple(data.values()))
                page = page +1
            
            time.sleep(0.1)
            
            text = str(returnList).replace("[","").replace("]","")
            returnList.clear()
            searchSQL.SQL_insertIngredientPrice(text)
            text=""

    print(text)
    # url = url.format(startTime,endTime,marketName[0],page,api_key)
    # print(url)
    # response = requests.get(url)
    # if len(response.json()['Data']) == 0:
    #     print("沒囉")

    # with open(dirPath.format(marketName[0]),'w',encoding="utf-8") as fp:
    #     fp.write(response.text)
    #     fp.close()


def getEndTimeAndStartTime():
    endTime = datetime.date.today()
    #endTime = endTime + datetime.timedelta(days=)
    startTime = endTime + datetime.timedelta(days=-132)
    

    endTime = str(endTime).replace("-",".")
    startTime = str(startTime).replace("-",".")

    endTime = str(int(endTime.split(".",1)[0])-1911) +"."+ endTime.split(".",1)[1]
    startTime = str(int(startTime.split(".",1)[0])-1911) +"."+ startTime.split(".",1)[1]
    print(startTime,endTime)
    return startTime,endTime

getIngredientPriceJson()
#getEndTimeAndStartTime()