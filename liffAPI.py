import os
import searchSQL
import json
from flask import json

# 版本3
# 回傳全部食材 json
def responseIngredient(userID='None'):
    # 透過Line Bot API得到userName
    print(userID)
    userName = searchSQL.getUserName(userID)
    token = 'None'
    # 假如userID正確 就能得到userName
    if userName != 'None':
        searchSQL.SQL_checkUserExists(userID,userName)
        token =  searchSQL.SQL_createLiffToken(userID)
    else:
        userID = 'NotExists'
    # 查詢全部食材的 & 為不喜歡的食材打上mark
    sql_result = searchSQL.SQL_getIngredientAll(userID)

    # 用來觀察json格式對不對 
    dirPath = os.path.dirname(os.path.abspath(__file__)) + '/response_Json/'+'responseIndex.json'

    # 圖片連結的url
    url = 'https://misIntro.asuscomm.com:5001/ingredient/photo/{}.jpg'

    ingre_class = ""
    ingre_subClass = ""
    ingre_id = ""
    ingre_name = ""
    ingre_commName = ""
    ingre_selected = ""
    ingre_url = ""
    type_class = ['v','f','h','s','b']
    index_class = 0
    tmp = 0
    tmp_ingreName = ""
    # json開頭
    text = '{{"userID":"{}","userName":"{}","token":"{}","kinds":['.format(userID,userName,token)
    for i , line in enumerate(sql_result):
        if tmp_ingreName != line[3]:
            tmp_ingreName = line[3]
            if ingre_class != line[0]:
                ingre_class = line[0]
                ingre_subClass = ""
                #print(ingre_class)
                if i == 0:
                    text = text + '{{"class":"{}","className":"{}","content":['.format(type_class[index_class],ingre_class)
                    index_class = index_class +1
                else:
                    text = text[:-1] + ']}]},'
                    text = text + '{{"class":"{}","className":"{}","content":['.format(type_class[index_class],ingre_class)
                    index_class = index_class +1
                    tmp = 0
            if ingre_subClass != line[1]:
                ingre_subClass = line[1]
                #print("\t"+ingre_subClass)
                if tmp == 0:
                    text = text + '{{"type":{},"typeName":"{}","ingredients":['.format(tmp,ingre_subClass)
                    tmp = tmp +1
                else:
                    text = text[:-1] + ']},'
                    text = text + '{{"type":{},"typeName":"{}","ingredients":['.format(tmp,ingre_subClass)
                    tmp = tmp +1
            ingre_id = line[2]
            ingre_name = line[3]
            if str(line[4]) == "None":
                ingre_commName = ""
            else:
                ingre_commName = line[4]
            ingre_url = url.format(ingre_id)
            if str(line[5]) == "None":
                ingre_selected = 'true'
            else:
                ingre_selected = 'false'
            text = text + '{{"id":"{}","name":"{}","commName":"{}","like":{},"imgUrl":"{}"}},'\
                .format(ingre_id,ingre_name,ingre_commName,ingre_selected,ingre_url)
            #print(f"\t\t{ingre_id} {ingre_name} {ingre_url} {ingre_selected}")
        else:
            tmp_ingreName = line[3]
    text = text[:-1] + ']}]}]}'
    with open(dirPath,'w',encoding='utf-8') as fp:
        #print(type(json.loads(text)))
        fp.write(text)
        fp.close()
    return text

def updateUserUnlike(userID,token,unlikeIngredientID):
    tokenStatus = searchSQL.SQL_checkLiffToken(userID,token)
    values = ""
    if tokenStatus == True:
        for i in unlikeIngredientID:
            values = values + f",('{userID}','{i}')"
        values = values.split(',',1)[1]
        searchSQL.SQL_insertNewUnlikeIngr(values)
        return "更新使用者不喜歡食材成功"
    else:
        return "更新使用者不喜歡食材失敗哭哭"
        



# # 版本1
# # 回傳全部食材 json
# def responseIngredient(userID='None'):
#     # 透過Line Bot API得到userName
#     userName = searchSQL.getUserName(userID)
#     # 假如userID正確 就能得到userName
#     if userName != 'Null':
#         searchSQL.SQL_checkUserExists(userID,userName)

#     # 查詢全部食材的 & 為不喜歡的食材打上mark
#     sql_result = searchSQL.SQL_getIngredientAll(userID)

#     # # 用來觀察json格式對不對 
#     # dirPath = os.path.dirname(os.path.abspath(__file__)) + '/response_Json/'+'responseIndex.json'

#     # 圖片連結的url
#     url = 'https://misIntro.asuscomm.com:5001/ingredient/photo/{}.jpg'

#     ingre_class = ""
#     ingre_subClass = ""
#     ingre_id = ""
#     ingre_name = ""
#     ingre_url = ""
#     ingre_selected = ""

#     tmp = 0
#     # json開頭
#     text = '{{"userID":"{}","content":['.format(userID)
#     #print(len(list1))
#     for i , line in enumerate(sql_result):
#         if ingre_class != line[0]:
#             ingre_class = line[0]
#             ingre_subClass = ""
#             #print(ingre_class)
#             if i == 0:
#                 text = text + '{{"class":"{}","classContent":['.format(ingre_class)
#             else:
#                 text = text[:-1] + ']}]},'
#                 text = text + '{{"class":"{}","classContent":['.format(ingre_class)
#                 tmp = 0
#         if ingre_subClass != line[1]:
#             ingre_subClass = line[1]
#             #print("\t"+ingre_subClass)
#             if tmp == 0:
#                 tmp = tmp +1
#                 text = text + '{{"subClass":"{}","subClassContent":['.format(ingre_subClass)
#             else:
#                 text = text[:-1] + ']},'
#                 text = text + '{{"subClass":"{}","subClassContent":['.format(ingre_subClass)
#         ingre_id = line[2]
#         ingre_name = line[3]
#         ingre_url = url.format(ingre_id)
#         if str(line[4]) == "None":
#             ingre_selected = 'false'
#         else:
#             ingre_selected = 'true'
#         text = text + '{{"id":"{}","name":"{}","imgUrl":"{}","selected":{}}},'\
#             .format(ingre_id,ingre_name,ingre_url,ingre_selected)
#         #print(f"\t\t{ingre_id} {ingre_name} {ingre_url} {ingre_selected}")
#     text = text[:-1] + ']}]}]}'
#     return text
#     # with open(dirPath,'w',encoding='utf-8') as fp:
#     #     #print(type(json.loads(text)))
#     #     fp.write(text)
#     #     fp.close()

# # 版本2
# # 回傳全部食材 json
# def responseIngredient(userID='None'):
#     # 透過Line Bot API得到userName
#     userName = searchSQL.getUserName(userID)
#     # 假如userID正確 就能得到userName
#     if userName != 'Null':
#         searchSQL.SQL_checkUserExists(userID,userName)
#     else:
#         userID = 'None'
#     # 查詢全部食材的 & 為不喜歡的食材打上mark
#     sql_result = searchSQL.SQL_getIngredientAll(userID)

#     # # 用來觀察json格式對不對 
#     dirPath = os.path.dirname(os.path.abspath(__file__)) + '/response_Json/'+'responseIndex.json'

#     # 圖片連結的url
#     url = 'https://misIntro.asuscomm.com:5001/ingredient/photo/{}.jpg'

#     ingre_class = ""
#     ingre_subClass = ""
#     ingre_id = ""
#     ingre_name = ""
#     ingre_commName = ""
#     ingre_selected = ""
#     ingre_url = ""
#     type_class = ['v','f','s','h','b']
#     index_class = 0
#     tmp = 0
#     text = ''
#     #print(len(list1))
#     for i , line in enumerate(sql_result):
#         if ingre_class != line[0]:
#             ingre_class = line[0]
#             ingre_subClass = ""
#             #print(ingre_class)
#             if i == 0:
#                 text = text + '[{{"class":"{}","content":['.format(type_class[index_class])
#                 index_class = index_class +1
#             else:
#                 text = text[:-1] + ']}]},'
#                 text = text + '{{"class":"{}","content":['.format(type_class[index_class])
#                 index_class = index_class +1
#                 tmp = 0
#         if ingre_subClass != line[1]:
#             ingre_subClass = line[1]
#             #print("\t"+ingre_subClass)
#             if tmp == 0:
#                 text = text + '{{"type":{},"typeName":"{}","ingredients":['.format(tmp,ingre_subClass)
#                 tmp = tmp +1
#             else:
#                 text = text[:-1] + ']},'
#                 text = text + '{{"type":{},"typeName":"{}","ingredients":['.format(tmp,ingre_subClass)
#                 tmp = tmp +1
#         ingre_id = line[2]
#         ingre_name = line[3]
#         if str(line[4]) == "None":
#             ingre_commName = ""
#         else:
#             ingre_commName = line[4]
#         ingre_url = url.format(ingre_id)
#         if str(line[5]) == "None":
#             ingre_selected = 'true'
#         else:
#             ingre_selected = 'false'
#         text = text + '{{"id":"{}","name":"{}","commName":"{}","like":{},"imgUrl":"{}"}},'\
#             .format(ingre_id,ingre_name,ingre_commName,ingre_selected,ingre_url)
#         #print(f"\t\t{ingre_id} {ingre_name} {ingre_url} {ingre_selected}")
#     text = text[:-1] + ']}]}]'
#     # with open(dirPath,'w',encoding='utf-8') as fp:
#     #     #print(type(json.loads(text)))
#     #     fp.write(text)
#     #     fp.close()
#     return text


