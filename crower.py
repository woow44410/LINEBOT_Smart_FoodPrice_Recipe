import urlSearch
import getRecipe
import json

def crower(keyword,page):
    urls = urlSearch.getUrl(keyword,page)
    recipes = []
    for url in urls:
        relay = getRecipe.getRecipe(url)
        if relay != True:
            recipes.append(relay)
    return recipes

if __name__ == '__main__':
    print(json.dumps(crower('花椰菜',1),ensure_ascii=False))