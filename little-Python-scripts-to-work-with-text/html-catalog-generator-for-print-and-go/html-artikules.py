# -*- coding: utf-8 -*-
#Помещаем скрипт в папку с картинками и в эту же папку помещаем текстовый файл, где на каждой строчке
#разделёные табуляцией артикул и имя картинки продукта
#если в папке есть файл с названием из текстового файла то скрипт запишет в выходной html файл его с артикулом
#
#скрипт предназначен для созданий файла для печати товаров с отображением артикула товара и фотографии

import re
import os

startFile = 'art-images.txt'

def getStartData():
    startData = []
    f = open(startFile)
    for line in f:
        result = re.findall("(.*?)(\t|$)", line)
        imageFileName = re.findall(r"[^/]*?\..*?$", result[1][0])
        dic = {'art': result[0][0], 'img': imageFileName[0]}
        startData.append(dic)
    f.close()
    return startData

startData = getStartData()

html = '<!doctype html><html lang="en"><head><style>div.image {display: inline-block;border: 1px solid black;margin: 2px;padding: 2px;} div.image img{width: 200px;} div.image h1 {font-size: 15px;}</style><meta charset="UTF-8"></head><body>'
listing = os.listdir(os.path.dirname(os.path.realpath(__file__)))
for file in listing:
    for product in startData:
        if (file.lower() == product['img'].lower()):
            html += '<div class="image"><img src="' + file + '" alt=""><h1>' + product['art'] + '</h1></div>'


html += '</body></html>'

f2 = open('index.htm', 'a')
f2.write(html)
f2.close()
