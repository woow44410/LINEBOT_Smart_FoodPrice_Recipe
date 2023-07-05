import connectMSSQL
import openFile

# 將大種類寫入 ingredient_class
def createIngredientClassSQL():
    try:
        cursor = connectMSSQL.connectMsSQL()
        text = openFile.openIngredientAllKinds()
        ingredient_class = ['vege','fruit','meal','fish','bean']
        ingredient_className = ['蔬菜','水果','家禽（畜）','海鮮','豆製品']
        query = "Insert into ingredient_class (class_id,class_name,subClass_name) values"
        class_id = 1
        # 取得每一筆的id和名稱
        for i in range(len(text)):
            arr = []
            for j in range(len(text[i]['content'])):
                if i == 0 and j == 0 :
                    # 第一個前面不用有 ,
                    className =  ingredient_className[i]
                    subClassName = text[i]['content'][j]['typeName']
                    query = query + "('{:0>3d}{}','{:s}','{:s}')".format(class_id,ingredient_class[i],className,subClassName)
                else:
                    arr.append(text[i]['content'][j]['typeName'])
            for k in range(len(arr)):
                class_id = class_id +1
                className =  ingredient_className[i]
                subClassName = arr[k]
                query = query + ",('{:0>3d}{}','{:s}','{:s}')".format(class_id,ingredient_class[i],className,subClassName)
        query = query +";"
        cursor.execute(query)
        cursor.close()
    except:
        print("SQL失敗")

#寫入全部食材到 ingredient
def createIngredientSQL():
    try:
        cursor = connectMSSQL.connectMsSQL()
        text = openFile.openIngredientAllKinds()
        
        ingredient_class = ['vege','fruit','meal','fish','bean']
        query = "Insert into ingredient (serial_no,class_id,id,name,commName) values"
        serial_no = 0
        class_id = 0
        for i in range(len(text)):
            for j in range(len(text[i]['content'])):
                class_id = class_id +1
                id = []
                name = []
                commName = []
                
                for k in range(len(text[i]['content'][j]['ingredient'])):
                    tmp = text[i]['content'][j]['ingredient'][k]
                    id.append(tmp['id'])
                    name.append(tmp['name'])
                    tmpCommName = ""
                    # 如果commName裡面有 "-" 就拿"-"前面的字
                    if tmp['commName'] == None:
                        commName.append(tmp['name'].split("-",1)[0])
                    elif "-" in tmp['name']:
                        print("哈哈")
                        tmpCommName = tmp['commName'] +","+tmp['name'].split("-",1)[0]
                        print(tmpCommName)
                        commName.append(tmpCommName)
                    else:
                        commName.append(tmp['commName'])

                    if(i==0 and j==0 and k ==0):
                        serial_no = serial_no + 1
                        query = query + "({},'{:0>3}{}','{}','{}','{}')"\
                            .format(serial_no,class_id,ingredient_class[i],id[k],name[k],commName[k])
                    else:
                        serial_no = serial_no + 1
                        query = query + ",({},'{:0>3}{}','{}','{}','{}')"\
                            .format(serial_no,class_id,ingredient_class[i],id[k],name[k],commName[k])
                
        query = query +";"
        print(query)
        cursor.execute(query)
        cursor.close()
    except:
        print("SQL失敗")

createIngredientSQL()