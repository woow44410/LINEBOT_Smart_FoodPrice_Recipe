import pymssql
# 連接SQL
def connectMsSQL():
    db_settings = {
        "server": "DESKTOP-U8UBC6O",
        "user": "DragonCode",
        "password": "handsome55",
        "database": "LinebotSchoolProject",
        'charset': "utf8",
        'autocommit': True
    }
    try:
        # 建立Connection物件
        conn = pymssql.connect(**db_settings)
        cursor = conn.cursor()
        return cursor
    except Exception as ex:
        print(ex)
