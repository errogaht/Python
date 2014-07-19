# -*- coding: utf-8 -*-
#Помещаем скрипт в папку с картинками
#если в папке есть jpg, png или gif файлы то будет создан html каталог этих файлов - картинка и название файла под ним
#
#скрипт предназначен для созданий файла для печати товаров с отображением имени картинки и самой картинки, удобен если например еть папка с фото товаров и нужно напечатать их все для сверки наличия на складе

import re
import os



html = '<!doctype html><html lang="en"><head><style>div.image {display: inline-block;border: 1px solid black;margin: 2px;padding: 2px;} div.image img{width: 200px;} div.image h1 {font-size: 15px;}</style><meta charset="UTF-8"></head><body>'
listing = os.listdir(os.path.dirname(os.path.realpath(__file__)))
for file in listing:
    match = re.search(r"\.([^.]*$)", file)
    if match:
        result = match.group(1)
    else:
        result = ""
    if (result.lower() == 'jpg' or result.lower() == 'jpeg' or result.lower() == 'png' or result.lower() == 'gif'):
        html += '<div class="image"><img src="' + file + '" alt=""><h1>' + file + '</h1></div>'


html += '</body></html>'

f2 = open('index.htm', 'a')
f2.write(html)
f2.close()
