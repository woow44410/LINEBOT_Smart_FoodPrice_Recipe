#把食譜內容抓下來 url->
import os,json,requests,re,sys,traceback,time
from lxml import etree
from os.path import join

path_prefix = os.path.dirname(os.path.abspath(__file__)) + '/Data'

def dataChecker(data):
    if isinstance(data,list) and len(data) > 0:
        return data[0].strip()
    else:
        return None

def getRecipe(url,key):
    #正常retuen recept
    #api 到上限 return False
    #沒食譜 return True
    proxies = {
                "http": f"http://scraperapi:{key}@proxy-server.scraperapi.com:8001"
            }
    response = requests.get(url,headers=headers, data=payload, proxies=proxies, verify=False)
    content = response.content.decode("utf8")
    if('est limit' in content):
        return False
    html = etree.HTML(content)

    recipe = {}
    recipe['id'] = re.findall('/([0-9]*)',url)[-1]
    recipe['name'] =dataChecker(
        html.xpath('//*[@id="recipe-name"]/text()'))
    recipe['img'] = dataChecker(
        html.xpath('//*[@id="o-wrapper"]/div[3]/div[2]/main/article/div[2]/div[1]/div/div[1]/div/a/img/@src'))
    recipe['portion'] = dataChecker(
        html.xpath('//*[@id="o-wrapper"]/div[3]/div[2]/main/article/div[2]/div[2]/div[1]/div/div/span[1]/text()'))
    recipe['time'] = dataChecker(
        html.xpath('//*[@id="o-wrapper"]/div[3]/div[2]/main/article/div[2]/div[2]/div[2]/div/span[1]/text()'))
    recipe['calorie'] = None
    recipe['Ingredients'] = []
    for d in html.xpath('//*[@class="ingredients-groups"]/div/div/div'):
        Ingredient = d.xpath('./div/a/text()')[0].strip()
        weight = d.xpath('./div[2]/text()')[0].strip()
        recipe['Ingredients'].append([Ingredient,weight])
    recipe['url'] = url

    if recipe['name'] == None:
        return True
    return recipe

def getRecipe(url):
    #正常retuen recept
    #沒食譜 return True
    response = requests.get(url,headers=headers, data=payload)
    content = response.content.decode("utf8")
    html = etree.HTML(content)

    recipe = {}
    recipe['id'] = re.findall('/([0-9]*)',url)[-1]
    recipe['name'] =dataChecker(
        html.xpath('//*[@id="recipe-name"]/text()'))
    recipe['img'] = dataChecker(
        html.xpath('//*[@id="o-wrapper"]/div[3]/div[2]/main/article/div[2]/div[1]/div/div[1]/div/a/img/@src'))
    recipe['portion'] = dataChecker(
        html.xpath('//*[@id="o-wrapper"]/div[3]/div[2]/main/article/div[2]/div[2]/div[1]/div/div/span[1]/text()'))
    recipe['time'] = dataChecker(
        html.xpath('//*[@id="o-wrapper"]/div[3]/div[2]/main/article/div[2]/div[2]/div[2]/div/span[1]/text()'))
    recipe['calorie'] = None
    recipe['Ingredients'] = []
    for d in html.xpath('//*[@class="ingredients-groups"]/div/div/div'):
        Ingredient = d.xpath('./div/a/text()')[0].strip()
        weight = d.xpath('./div[2]/text()')[0].strip()
        recipe['Ingredients'].append([Ingredient,weight])
    recipe['url'] = url

    if recipe['name'] == None:
        return True
    return recipe

def getKey(keyNum):
    with open(join(path_prefix,'proxyKey.txt')) as f:
        keys = f.read().split('\n')
    return keys[keyNum],len(keys)


with open(join(path_prefix,'recipes.json'),'r+',encoding='utf8') as saveFile:
    recipes = json.loads(saveFile.read())
with open(join(path_prefix,'url.txt'),'r+',encoding='utf8') as F:
    urls = F.read().split('\n')
urlLength = len(urls)
if not isinstance(recipes,list):
    print("saveFile 有問題")

payload={}
headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}

keyNum = 0
key , keylength = getKey(keyNum)

if __name__ == '__main__':
    for u, url in enumerate(urls):
        time.sleep(1)
        url = url.replace('https','http')
        attempt = 2
        while(attempt > 0):
            try:
                print(f'目前筆數:({u+1}/{urlLength}) 使用金鑰:({keyNum+1}/{keylength})\t\t',end='\r')
                res = getRecipe(url)
                if res == True: break
                if res == False:
                    attempt += 1
                    keyNum+=1
                    key,_ = getKey(keyNum)
                    continue
                recipes.append(res)
                break
            except Exception as e:
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                print('\n'+ errMsg)
                attempt -= 1
                time.sleep(1)
        if attempt <= 0:
            continue

        if(u % 1)==0:
            with open(join(path_prefix,'recipes.json'),'w+',encoding='utf8') as saveFile:
                saveFile.write(json.dumps(recipes,ensure_ascii=False))
            with open(join(path_prefix,'url.txt'),'w+',encoding='utf8') as F:
                F.write('\n'.join(urls[u+1:]))
    print('\n Finished!!')
    if u == urlLength:
        with open(join(path_prefix,'recipes.json'),'w+',encoding='utf8') as saveFile:
            saveFile.write(json.dumps(recipes,ensure_ascii=False))
        with open(join(path_prefix,'url.txt'),'w+',encoding='utf8') as F:
            F.write('\n'.join(urls[u+1:]))
