# -*- coding: utf-8 -*-
#######################
#Скрипт поедает два текстовых файла, первый с id и картинкой разделённые табом товара со вкладки products
#другой — список addiditional images
#формат названий файлов картинок должен быть определённым - modelname-34.jpg например
#у каждой модели может быть несколько фотографий и каждая обозначается числом через минус
#на выходе получаем список всех addiditional images но с проставленными айдишниками
#скрипт смотрит список товаров с картинкой и айдишником вытаскивает оттуда название модели и для всех фоток этой модели ставит айдишник
#######################

import re
import os

# Settings
imagesAndID         = 'productsImages.txt'
addiditionalImages  = 'addiditionalImages.txt'
resultFile          = 'result.txt'

# Functions
def getStartImages():
    startImages = []
    f = open(imagesAndID)
    for line in f:
        # data/catalog/569/mariela-43-1.jpg, imageFileName = mariela-43-1.jpg
        result = re.findall("(.*?)(\t|$)", line)
        imageFileName = re.findall(r"[^/]*?\..*?$", result[1][0])
        dic = {'id': result[0][0], 'fileName': imageFileName[0]}
        startImages.append(dic)
    f.close()
    return startImages


def getAddImages():
    addImages = []
    f = open(addiditionalImages)
    for line in f:
        # data/catalog/569/mariela-43-1.jpg, imageFileName = mariela-43-1.jpg
        line = line.strip()
        imageFileName = re.findall(r"[^/]*?\..*?$", line)
        dic = {'id': '', 'fileName': imageFileName[0], 'originalName': line}
        addImages.append(dic)
    f.close()
    return addImages


def modelFrom(image):
    # mariela-40-6.jpg, model = mariela-40
    result  = re.findall(r"(.*)-\d+?\..*?$", image['fileName'])
    model   = result[0]
    return model

# Work
startImages     = getStartImages()
addImages       = getAddImages()

out = []

for startImage in startImages:
    for addImage in addImages:
        if ( modelFrom(addImage) == modelFrom(startImage) ):
            dic = {'id': startImage['id'], 'file': addImage['originalName']}
            out.append(dic)

string = ''
for item in out:
    string += item['id'] + "\t" + item['file'] + "\n"

f = open(resultFile, 'a')
f.write(string)
f.close()