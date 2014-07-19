# -*- coding: utf-8 -*-


import re
import logging
import urllib
import string
import random
import os
import urlparse
from grab import Grab
from pyexcelerate import Workbook, Style, Font
"""
logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
"""


data = \
    {
        'items': [
            {'name': 'title',           'type': 'text',     'xpath': './/div[@id="center"]/h1'},
            {'name': 'adres',           'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Располож' + '")]/following::text()[2]'},
            {'name': 'type',            'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Ти' + '")]/following::text()[2]'},
            {'name': 'vid',             'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Ви' + '")]/following::text()[2]'},
            {'name': 'new-price',       'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Цен' + '")]/following::text()[2]'},
            {'name': 'old-price',       'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Цен' + '")]/following::text()[3]'},
            {'name': 'bassein',         'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Бас' + '")]/following::text()[2]'},
            {'name': 'spalni',          'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Спал' + '")]/following::text()[2]'},
            {'name': 'ploshad-zemli',   'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Прощ' + '")]/following::text()[2]'},
            {'name': 'o-ploshad',       'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Общ' + '")]/following::text()[2]'},
            {'name': 'j-ploshad',       'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Жил' + '")]/following::text()[2]'},
            {'name': 'balkon',          'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Бал' + '")]/following::text()[2]'},
            {'name': 'terassa',         'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Тера' + '")]/following::text()[2]'},
            {'name': 'sad',             'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Са' + '")]/following::text()[2]'},
            {'name': 'kunia',           'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Кух' + '")]/following::text()[2]'},
            {'name': 'vanna',           'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Ван' + '")]/following::text()[2]'},
            {'name': 'mebel',           'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Меб' + '")]/following::text()[2]'},
            {'name': 'etajnost',        'type': 'text',     'xpath': './/div[@id="center"]//table//tr/th[substring-after(text(), "' + u'Эта' + '")]/following::text()[2]'},
            {'name': 'description',     'type': 'text',     'xpath': './/div[@id="content"]//div/p'},
            {'name': 'images',          'type': 'text',     'xpath': './/ul[@class="photos"]/li/a/@href'},
            {'name': 'cat1',            'type': 'text',     'xpath': './/*[@id="breadcrumbs"]/a[2]'},
            {'name': 'cat2',            'type': 'text',     'xpath': './/*[@id="breadcrumbs"]/a[3]'},
            {'name': 'cat3',            'type': 'text',     'xpath': './/*[@id="breadcrumbs"]/a[4]'},
            {'name': 'cat4',            'type': 'text',     'xpath': './/*[@id="breadcrumbs"]/a[5]'}
        ],
        'links': [
            'http://site.com/item1',
            'http://site.com/item2',
        ]
    }

opt = {'delimiter': ';'}

g = Grab(connect_timeout=5, userpwd='user:pass', debug_post='True', log_dir='log', headers={'Accept-Language':    'ru,en;q=0.8'})


def parse(xpath, type):
    out = ''
    if (type == 'text'):
        try:
            result = g.doc.select(xpath)
            length = len(result.selector_list)
            if length > 1:
                i = 0
                for item in result:
                    i += 1
                    if (i == length):
                        out = out + item.text(smart=True)
                    else:
                        out = out + item.text(smart=True) + opt['delimiter']+ ' '

            elif length == 1:
                out = result.text(smart=True)
        except:
            pass
        return out

itemsCollection = []

# создаём заголовок таблицы
row = []
for item in data['items']:
    row.append(item['name'])
row.append('Original URL')
itemsCollection.append(row)

# сами данные парсинга
totalLinks = len(data['links'])
i = 0
for link in data['links']:
    i+=1
    g.go(link)
    row = []
    for item in data['items']:
        content = parse(item['xpath'], item['type'])
        row.append(content)
    row.append(link)
    itemsCollection.append(row)
    print '['+ str(i) +'/'+ str(totalLinks) +']'

wb = Workbook()
ws = wb.new_sheet("sheet name", data=itemsCollection)
ws.set_row_style(1, Style(font=Font(bold=True)))
wb.save("output.xlsx")

