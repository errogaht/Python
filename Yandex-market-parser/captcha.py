# -*- coding: utf-8 -*-

import time

import httplib
import urllib
import logging


def ripcaptcha(key, fn):
    # sending a captcha
    cap_id = send_cap(key, fn)
    if not cap_id:
        print 'Íå îòïðàâèëîñü'
        return

    # getting result
    status, text = get_cap_text(key, cap_id)
    print 'captcha defeated! ' + text
    return text

def main():
    key = 'ca0f318716570662e964bea13cc779d7'
    fn = 'image.gif'

    # sending a captcha
    cap_id = send_cap(key, fn)
    if not cap_id:
        print 'Íå îòïðàâèëîñü'
        return

    # getting result
    status, text = get_cap_text(key, cap_id)
    print text


def get_cap_text(key, cap_id):
    """ Waiting and getting captcha text """
    print('--- Get captcha text')
    logging.info('--- Get captcha text')
    time.sleep(5)

    res_url = 'http://ripcaptcha.com/res.php'
    res_url += "?" + urllib.urlencode({'key': key, 'action': 'get', 'id': cap_id})
    while 1:
        res = urllib.urlopen(res_url).read()
        if res == 'CAPCHA_NOT_READY':
            time.sleep(1)
            continue
        break

    res = res.split('|')
    if len(res) == 2:
        return tuple(res)
    else:
        return 'ERROR', res[0]


def send_cap(key, fn):
    """ sending captcha
		IN:
			key	- account key
			fn		- file name
		OUT:
			captcha id	- in case of success
			False	- in case of failure
	"""
    logging.info('--- Send captcha')
    print('--- Send captcha')
    data = open(fn, 'rb').read()

    # data boundary
    boundary = '----------OmNaOmNaOmNamo'

    # building POST request
    body = '''--%s
Content-Disposition: form-data; name="method"

post
--%s
Content-Disposition: form-data; name="key"

%s
--%s
Content-Disposition: form-data; name="file"; filename="capcha.jpg"
Content-Type: image/pjpeg

%s
--%s--

''' % (boundary, boundary, key, boundary, data, boundary)

    headers = {'Content-type': 'multipart/form-data; boundary=%s' % boundary}
    # connecting
    h = httplib.HTTPConnection('ripcaptcha.com')
    # sending request
    h.request("POST", "/in.php", body, headers)
    # receiving answer and analyzing it
    resp = h.getresponse()
    data = resp.read()
    h.close()
    if resp.status == 200:
        cap_id = int(data.split('|')[1])
        return cap_id
    else:
        print('Captcha not send: %s %s' % (resp.status, resp.reason))
        logging.error('Captcha not send: %s %s' % (resp.status, resp.reason))
        return False

"""
if __name__ == "__main__":
    main()"""