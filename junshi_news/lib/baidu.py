# -*-coding=utf-8-*-
import json
import http.client
import hashlib
import urllib.parse
import random


class BaiduModel:

    def __init__(self, app_id, secret_key, from_lang='zh', to_lang='en'):
        self.app_id = app_id
        self.secret_key = secret_key
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.my_url = '/api/trans/vip/translate'

    def translate(self, context):
        salt = random.randint(32768, 65536)
        sign = self.app_id + context + str(salt) + self.secret_key
        m1 = hashlib.md5(sign.encode('utf-8'))
        sign = m1.hexdigest()
        my_url = self.my_url + '?appid=' + self.app_id + '&q=' + urllib.parse.quote(context) + \
                 '&from=' + self.from_lang + '&to=' + self.to_lang + '&salt=' + str(salt) + '&sign=' + sign
        http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
        while True:
            try:
                http_client.request('GET', my_url)
                # response是HTTPResponse对象
                response = http_client.getresponse()
                result = response.read().decode('unicode-escape')
                data = json.loads(result)
                translate = data['trans_result'][0]['dst']
                return translate
            except Exception:
                 continue
            finally:
                if http_client:
                    http_client.close()
