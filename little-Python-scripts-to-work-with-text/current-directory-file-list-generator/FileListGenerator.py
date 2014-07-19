# -*- coding: utf-8 -*-
import re
import os

#Настройки
excludeExtensionList = ["py", "ds_store", "txt"]
path = os.path.dirname(os.path.realpath(__file__))
listing = os.listdir(path)

outData = ''
for file in listing:
    match = re.search(r"\.([^.]*$)", file)
    if match:
        result = match.group(1)
    else:
        result = ""
    ext = result.lower()
    if ext not in excludeExtensionList:
        outData += file + '\n'


f2 = open('fileList.txt', 'a')
f2.write(outData)
f2.close()
