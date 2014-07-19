# -*- coding: utf-8 -*-
from grab import Grab
import re
import urlparse
import urllib
import os
from translite import transliterate as trans



def GetAllLinksFromString(html, url):
    #возвращает список со всеми ссылками найденными в html
    #необходимо указать url по которомы данный текст был получен

    result = re.findall('(?i)href="([^<>"]*)"', html)
    # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    netloc = urlparse.urlsplit(url)[1]
    result = list(set(result))
    result2 = []
    for item in result:
        item = re.sub("^/", "", item)
        item = re.sub("/$", "", item)
        item = re.sub("^#$", "", item)
        if re.search("http://", item):
            pass
        else:
            if item == '':
                item = 'http://' + netloc
            else:
                item = 'http://' + netloc + '/' + item
        result2.append(item)
    result2 = list(set(result2))
    return result2


def dumpL(list):
    f = open('links.txt', 'w')
    out = ''
    for url in list:
        out = out + url + '\n'
    f.write(out)
    f.close()


def dump(g):
    f = open('out.html', 'w')
    f.write(g.response.body)
    f.close()


def golink(g, text):
    url = g.find_link(text)
    g.go(url)


def GetFileExtFromURL(fullpath):
    (root, ext) = os.path.splitext(urlparse.urlparse(fullpath).path)
    return ext


def StringForFilename(string):
    string = trans(string)
    string = re.sub(r"[\s]", "-", string)
    string = re.sub("[^qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-]", "", string)
    return string

prefix = 0


def deleteNumerators(path):
    listing = os.listdir(path)
    for file in listing:
        new = re.sub(r"(.*)-\d+?(\.[^.]+?)$", r"\1\2", file)
        new = path + "\\" + new
        old = path + "\\" + file
        try:
            os.rename(old, new)
        except:
            pass


def SaveImageYandex(text, imageCount, path, w='800', h='600'):
    global prefix
    prefix += 1
    g = Grab(connect_timeout=5, userpwd='user:pass', debug_post='True', log_dir='log', headers={'Accept-Language':    'ru,en;q=0.8'})
    query = urllib.urlencode({'text': text.encode('utf-8'), 'iw': w, 'ih': h})
    url = 'http://images.yandex.ru/yandsearch?isize=gt&itype=jpg&'+query
    g.go(url)
    image_number = 0
    f2 = open('out.txt', 'a')
    filename = str(prefix) + '-' + StringForFilename(text) + '.jpg'
    f2.write(filename + '\n')
    f2.close()
    while image_number < imageCount:
        image_number += 1
        tmp = g.doc.select('//html/body/div[2]/div/div[2]/div[2]/div[1]/div[contains(@class, "b-images-item")]['
                           + str(image_number) + ']').attr('onclick')
        match = re.search(r'"fullscreen":\{"url":"(.*?)"', tmp)
        if match:
            image_URL = match.group(1)
            print str(image_number) + '. ' + image_URL
            ext = GetFileExtFromURL(image_URL)
            filename = str(prefix) + '-' + StringForFilename(text) + '-' + str(image_number) + '.jpg'
            try:
                patht = os.path.join(path, filename)
                print patht
                urllib.urlretrieve(image_URL, patht)
            except:
                pass
        else:
            print 'Cant find image for this query ' + str(image_number)

"""
f = open('query.txt')
for line in f.readlines():
    SaveImageYandex(u''+line, 30, 'D:\data\Teterin\programming\python/parce-cat/dbrides', '1000', '1000')
f.close()
"""
SaveImageYandex(u'свадебное платье', 30, 'D:\data\Teterin\programming\python/parce-cat/brides', '1000', '1000')

# deleteNumerators('D:\Dropbox\Teterin\programming\python\parce-cat\img')