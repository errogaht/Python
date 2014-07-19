# -*- coding: utf-8 -*-

CATEGORIES = 'cat_id-cat_names.txt'
PRODUCTS = 'products_id-cat_id.txt'
OUT = 'result.txt'



def getCategories(path):
    categories = []
    f = open(path)
    for line in f:
        result = line.split("\t")
        dic = {'ID': result[0].strip(), 'Name': result[1].strip()}
        categories.append(dic)
    f.close()
    return categories


def getProducts(path):
    products = []
    f = open(path)
    for line in f:
        result = line.split("\t")
        result[1] = result[1].strip()
        categoriesList = [x.strip() for x in result[1].split(",")]
        dic = {'ID': result[0].strip(), 'Categories': categoriesList}
        products.append(dic)
    f.close()
    return products



p = getProducts(PRODUCTS)
c = getCategories(CATEGORIES)

def replace(product):

    categories = []
    for pcategory in product['Categories']:
        for category in c:
            if (category['ID'] == pcategory):
                categories.append(category['Name'])
    return {'ID': product['ID'], 'Categories': categories}



p = [replace(product) for product in p]

out = ""
for product in p:
    cats = ""
    l = len(product['Categories'])
    i = 0
    for cat in product['Categories']:
        i+=1
        if (i != l):
            cats += cat + ","
        else:
            cats += cat
    out += str(product['ID']) + "\t" + cats + "\n"

f = open(OUT, 'w')
f.write(out)
