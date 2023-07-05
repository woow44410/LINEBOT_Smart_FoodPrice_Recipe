import os,json,requests,re,sys,traceback,time
from lxml import etree
from os.path import join
path_prefix = os.path.dirname(os.path.abspath(__file__)) + '/Data'

def getUrl(keyword,page):
    urlSearch = f'http://icook.tw/search/{keyword}/?page=page'
    payload={}
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    response = requests.get(urlSearch,headers=headers, data=payload)
    content = response.content.decode("utf8")
    if('est limit' in content):
        return False
    html = etree.HTML(content)
    urls = []
    for div in html.xpath('//*[@class="browse-recipe-item"]/a/@href'):
        urls += ['http://icook.tw/'+div.strip()]

    return urls

def getSerialUrl():
    urls = [f'https://icook.tw/recipes/{serial}' for serial in range(31000,35000)]
    return urls

#花椰菜
if __name__=='__main__':
    urls = []
    for i in range(1,10):
        urls += getUrl('花椰菜',i)
    with open(join(path_prefix,'url.txt'),'w',encoding='utf8') as F:
        F.write('\n'.join(urls))