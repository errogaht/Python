# -*- coding: utf-8 -*-
import re
import os


filename = os.path.basename(__file__)



match = re.search(r"(.*)\.([^\.]*$)", filename)
if match:
    filename = match.group(1)
else:
    filename = ""


path = os.path.dirname(os.path.realpath(__file__))
listing = os.listdir(path)
i = 0
for file in listing:
    i += 1
    match = re.search(r"\.([^.]*$)", file)
    if match:
        result = match.group(1)
    else:
        result = ""
    ext = result.lower()
    if (ext == 'jpg' or ext == 'jpeg' or ext == 'png' or ext == 'gif'):
        new = filename + '-' + str(i)
        new = path + "\\" + new + '.' + ext
        old = path + "\\" + file
        try:
            os.rename(old, new)
        except:
            pass

