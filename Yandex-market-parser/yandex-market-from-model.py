# -*- coding: utf-8 -*-
import re
import urllib
import string
import random
import os
import urlparse
from grab import Grab
from captcha import ripcaptcha as ripcaptcha


# static options
opt = {'last_pid': 1,
       'lid': u'1',
       'parse_images': True,
       'imgServerPath': 'catalog/mobile/',
       'prjPath': 'D:\Data\Teterin\programming\python\parce-cat\data2',
       'quantity': u'1000', 'requires_shipping': u'yes', 'weight': u'1', 'unit': u'г', 'length': u'0', 'width': u'0',
       'height': u'0', 'length_unit': u'мм', 'status_enabled': u'true', 'language_id': u'1', 'stock_status_id': u'7',
       'store_ids': u'0', 'subtract': u'true', 'minimum': u'1'}

# parser options
popt = {'bimage': '//table[@id="model-pictures"]//span[@class="b-model-pictures__big"]/a/@href',
        'simages': '//table[@id="model-pictures"]//span[@class="b-model-pictures__small"]/a/@href',
        'title': '//h1[contains(@class, b-page-title)]',
        'yaMarket_specs_Values': '//table[@class="b-properties"]/tbody/tr/td[@class="b-properties__value"]',
        'yaMarket_specs_Titles': '//table[@class="b-properties"]/tbody/tr/th'}

captcha_opt = {'key': 'ca0f318716570662e964bea13cc779d7'}


def goLink(g, text):
    url = g.find_link(text)
    GoUrlYandexCaptcha(g, url)

def GetFileExtFromURL(fullpath):
    sub = [urlparse.urlparse(fullpath).path, urlparse.urlparse(fullpath).params, urlparse.urlparse(fullpath).query]
    for subject in sub:
        match = re.search(r"(\.[\w]+$)", subject)
        if match:
            ext = match.group(1)
            break
    return ext

def id_generator(size=30, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# get list of links to parse
def getStartModels(path):
    start_links = []
    f = open(path)
    for line in f:
        result = re.findall("(.*?)(\t|$)", line)
        dic = {'pid': result[0][0], 'model': result[1][0]}
        start_links.append(dic)
    f.close()
    return start_links
    # мы добавили в список links все строки из входного файла, превратив каждую из них в словарь с нужными параметрами

# create list of collums
class o:
    product_id = 0
    name = 1
    categories = 2
    main_categories = 3
    sku = 4
    upc = 5
    ean = 6
    jan = 7
    isbn = 8
    mpn = 9
    location = 10
    quantity = 11
    model = 12
    manufacturer = 13
    image_name = 14
    requires_shipping = 15
    price = 16
    points = 17
    date_added = 18
    date_modified = 19
    date_available = 20
    weight = 21
    unit = 22
    length = 23
    width = 24
    height = 25
    length_unit = 26
    status_enabled = 27
    tax_class_id = 28
    viewed = 29
    language_id = 30
    seo_keyword = 31
    description = 32
    meta_description = 33
    meta_keywords = 34
    seo_title = 35
    seo_h1 = 36
    stock_status_id = 37
    store_ids = 38
    layout = 39
    related_ids = 40
    tags = 41
    sort_order = 42
    subtract = 43
    minimum = 44
c = [c for c in range(0, 45, 1)]
for item in c:
    c[item] = u''

# static option assigment
c[o.quantity] = opt['quantity']
c[o.requires_shipping] = opt['requires_shipping']
c[o.weight] = opt['weight']
c[o.unit] = opt['unit']
c[o.length] = opt['length']
c[o.width] = opt['width']
c[o.height] = opt['height']
c[o.length_unit] = opt['length_unit']
c[o.status_enabled] = opt['status_enabled']
c[o.language_id] = opt['language_id']
c[o.stock_status_id] = opt['stock_status_id']
c[o.store_ids] = opt['store_ids']
c[o.subtract] = opt['subtract']
c[o.minimum] = opt['minimum']


def SaveImage(url):
    ipath = opt['prjPath'] + '\img/'
    ext = GetFileExtFromURL(url)
    filename = id_generator() + ext
    g = Grab(connect_timeout=5, userpwd='user:pass', debug_post='True', log_dir='log', headers={'Accept-Language':    'ru,en;q=0.8'})
    try:
        g.download(url, ipath + filename)
        print filename + " saved"
        return opt['imgServerPath'] + filename
    except:
        return 'no image'


def YandexMarketSaveModelAttributes(g, pid):
    global opt
    global popt
    lid = opt['lid']
    f = open(opt['prjPath'] + '/attributes.txt', 'a')
    goLink(g, 'model-spec')
    valuesX = g.doc.select(popt['yaMarket_specs_Values'])
    values = []
    for value in valuesX:
        values.append(value.text())
    titleX = g.doc.select(popt['yaMarket_specs_Titles'])
    pos = 0
    attr_Group = ''
    for l in titleX:
        if l.attr('class') == 'b-properties__title':
            attr_Group = l.text()
            continue
        if l.attr('class') == 'b-properties__label b-properties__label-title':
            attr_name = l.text()
            attr_value = values[pos]
            pos += 1
            row = pid + '\t' + lid + '\t' + attr_Group + '\t' + attr_name + '\t' + attr_value
            f.write(row.encode('utf-8') + '\n')
    f.close()

def SaveCaptcha(url):
    ipath = opt['prjPath'] + '/tmp/'
    ext = GetFileExtFromURL(url)
    filename = id_generator() + ext
    g = Grab(connect_timeout=5, userpwd='user:pass', debug_post='True', log_dir='log', headers={'Accept-Language':    'ru,en;q=0.8'})
    try:
        g.download(url, ipath + filename)
        return ipath + filename
    except:
        return 'no image'


def defeat_captcha(captcha_img_url, captcha_opt):
    captcha_file = SaveCaptcha(captcha_img_url)
    return ripcaptcha(captcha_opt['key'], captcha_file)


def GoUrlYandexCaptcha(g, url):
    global captcha_opt
    g.go(url)
    try:
        title = unicode(g.doc.select('//title').text())
        text_to_search = u"^Ограничение доступа$"
        if re.search(text_to_search, title):
            print 'Captcha detected!'
            captcha_img_url = g.doc.select('//form/img/@src').text()
            captcha_text = defeat_captcha(captcha_img_url, captcha_opt)
            g.set_input('response', captcha_text)
            g.submit()
            g.go(url)
        else:
            pass
    except:
        print 'cant get title'

class productClass:
    global opt
    global popt
    title = ''
    bImage = ''
    sImages = []
    pid = ''

    def get(self, model):
        self.title = ''
        self.bImage = ''
        self.sImages = []
        self.pid = model['pid']
        g = Grab(connect_timeout=5, userpwd='user:pass', debug_post='True', log_dir='log', headers={'Accept-Language':    'ru,en;q=0.8'})
        if re.search("http://", model['model']):
            url = model['model']
            GoUrlYandexCaptcha(g, url)
        else:
            url = 'http://market.yandex.ru/'
            GoUrlYandexCaptcha(g, url)
            g.set_input('text', model['model'])
            g.submit()
        try:
            self.title = g.doc.select(popt['title']).text()
                # Сохраняем главное изображение
            if opt['parse_images']:
                try:
                    bimage = g.doc.select(popt['bimage'])
                    for image in bimage:
                        self.bImage = SaveImage(image.text())
                except:
                    self.bImage = ''

            # Сохраняем дополнительные изображения
                try:
                    sImages = g.doc.select(popt['simages'])
                    for image in sImages:
                        self.sImages.append(SaveImage(image.text()))
                except:
                    self.sImages = []

        # Go to model specifications
            try:
                YandexMarketSaveModelAttributes(g, model['pid'])
            except:
                print 'cant get model specs for pid=' + model['pid'] + ' model=' + model['model']
        except:
            print 'cant get model page for pid=' + model['pid'] + ' model=' + model['model']






def GetAllLinksFromString(html, url):
    #возвращает список со всеми ссылками найденными в html
    #необходимо указать url по которомы данный текст был получен
    links = re.findall('(?i)href="([^<>"]*)"', html)
    netloc = urlparse.urlsplit(url)[1]
    links = list(set(links))
    linksList = []
    for item in links:
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
        linksList.append(item.encode('utf-8'))
    linksList = list(set(linksList))
    return linksList


def getModelLink(modelName):
    g = Grab(connect_timeout=5, userpwd='user:pass', debug_post='True', log_dir='log', headers={'Accept-Language':    'ru,en;q=0.8'})
    url = 'http://market.yandex.ru/'
    g.go(url)
    try:
        paginatorHTML = g.doc.select(popt['pagination']).html()
        pagesLinks = GetAllLinksFromString(paginatorHTML, url)
    except:
        pagesLinks = []
    pagesLinks.append(url)
    pagesLinks = list(set(pagesLinks))
    pagesCount = pagesLinks.__len__()
    newPagesCount = 1
    while pagesCount != newPagesCount:
        lastPage = pagesLinks.__len__() - 1
        url = pagesLinks[lastPage]
        g.go(url)
        try:
            paginatorHTML = g.doc.select(popt['pagination']).html()
            newlinks = GetAllLinksFromString(paginatorHTML, url)
        except:
            newlinks = []
        for newlink in newlinks:
            pagesLinks.append(newlink)
        pagesLinks = list(set(pagesLinks))
        newPagesCount = pagesLinks.__len__()
    return pagesLinks


def GetProductsLinks(catPage):
    # тут нужно получить ссылки на продукты
    productsLinks = []
    g = Grab(connect_timeout=5, userpwd='user:pass', debug_post='True', log_dir='log', headers={'Accept-Language':    'ru,en;q=0.8'})
    url = catPage
    g.go(url)
    catalogs = g.doc.select(popt['catalog'])
    for catalog in catalogs:
        links = GetAllLinksFromString(catalog.html(), url)
        for link in links:
            productsLinks.append(link)
    productsLinks = list(set(productsLinks))
    return productsLinks

product = productClass()
# get links to products
start_models = getStartModels(opt['prjPath'] + '\start_links.txt')
for model in start_models:
    print 'try to parse pid=' + model['pid'] + ' ' + model['model']
    product.get(model)
    # тут сохраняем результаты парсинга:
    # 2. Save addiditional images
    if ['parse_images'] and product.sImages.__len__() > 0:
        f = open(opt['prjPath'] + '\images.txt', 'a')
        for img in product.sImages:
            f.write(str(product.pid) + '\t' + img + '\t' + '0' + '\n')
        f.close()
    # 3. Save product ROW
    # main options, unique for each product
    c[o.name] = product.title
    c[o.product_id] = product.pid
    c[o.image_name] = product.bImage
    row = ''
    # в с у нас сохранены все нужные полученные опции товара
    # сформируем строку для записи разделенную табом
    for col in c:
        row = row + col + '\t'
    f = open(opt['prjPath'] + '\products.txt', 'a')
    f.write(row.encode('utf-8') + '\n')
    f.close()


