from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import execjs
from urllib import parse
import time
import datetime
import requests
import json


class BaiDuModel:

    def __init__(self):
        # 请求头
        self.headers = {}

        # js 转码计算器
        self.ctx = execjs.compile("""
            function a(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}var C=null;var hash=function(r,_gtk){var o=r.length;o>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(o/2)-5,10)+r.substr(-10,10));var t=void 0,t=null!==C?C:(C=_gtk||"")||"";for(var e=t.split("."),h=Number(e[0])||0,i=Number(e[1])||0,d=[],f=0,g=0;g<r.length;g++){var m=r.charCodeAt(g);128>m?d[f++]=m:(2048>m?d[f++]=m>>6|192:(55296===(64512&m)&&g+1<r.length&&56320===(64512&r.charCodeAt(g+1))?(m=65536+((1023&m)<<10)+(1023&r.charCodeAt(++g)),d[f++]=m>>18|240,d[f++]=m>>12&63|128):d[f++]=m>>12|224,d[f++]=m>>6&63|128),d[f++]=63&m|128)}for(var S=h,u="+-a^+6",l="+-3^+b+-f",s=0;s<d.length;s++)S+=d[s],S=a(S,u);return S=a(S,l),S^=i,0>S&&(S=(2147483647&S)+2147483648),S%=1e6,S.toString()+"."+(S^h)}
            """)

        # 传输数据
        self.data = {
                'from':'zh',
                'to':'en',
                # 'query':'我爱你',
                'transtype':'realtime',
                'simple_means_flag':'3',
                # 'sign':'47194.285547',
                # 'token':'c2a19c5eaea2bd5a3f5c415f174c9e4a'
        }

        # headers
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Content-Length': '119',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'fanyi.baidu.com',
            'Origin': 'http://fanyi.baidu.com',
            'Referer': 'http://fanyi.baidu.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            # 'Cookie': 'from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1530773001; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1528181573,1530758962,1530772069,1530773001; locale=zh; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1460_26431_21084_22159; PSINO=7; BDSFRCVID=MiPsJeC62mIsR237hyH2hVwc3pDKvyjTH6aoigjMoNgau_Z8T3GREG0PjM8g0Kub19c7ogKK5mOTH65P; H_BDCLCKID_SF=tJIqVIt2JKt3qRcFq4cqhRkthxJeanLXKKOLVh6VLPOkeq8CD4czKpjXDNJ3hxkH2Ncf3KOM3pv-JJc2y5jHhPFsM4cyWtbKbGOzVU-b3MopsIJMMxFWbT8U5fKDq4tfaKviaK5EBMb1MC5Me4bK-TrLDGKqtU5; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; REALTIME_TRANS_SWITCH=1; SOUND_PREFER_SWITCH=1; SOUND_SPD_SWITCH=1; MCITY=-%3A; BAIDUID=C6404371DAAB9403AA9476EF257D6BF6:FG=1; BIDUPSID=C6404371DAAB9403AA9476EF257D6BF6; PSTM=1525884285'
        }

    def parse_content(self, content):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # 设置中文
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        headers = ''
        for (k,v) in self.headers.items():
            headers += '%s=%s; ' % (k, v)
        # print(headers)
        chrome_options.add_argument(headers)
        prefs = {'profile.managed_default_content_settings.images': 2, 'profile.default_content_settings.popups': 0}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('http://fanyi.baidu.com')
        html = driver.execute_script("return document.documentElement.outerHTML")
        gtk = re.findall(r'window.gtk = \'(.*)\'', html)[0]
        token = re.findall(r'token: \'(.*)\'', html)[0]
        sign = self.ctx.call('hash', content, gtk)
        self.data['query'] = content
        self.data['sign'] = sign
        self.data['token'] = token
        dict_cookies = driver.get_cookies()
        temp_cookies = self.parse_cookies(dict_cookies)
        # print(temp_cookies)
        BAIDUPSID = temp_cookies['BAIDUID']
        temp_cookies['BAIDUPSID'] = BAIDUPSID.strip(':FG=1')
        temp_cookies['PSTM'] = '1525884285'
        temp_cookies['BDSFRCVID'] = 'MiPsJeC62mIsR237hyH2hVwc3pDKvyjTH6aoigjMoNgau_Z8T3GREG0PjM8g0Kub19c7ogKK5mOTH65P'
        temp_cookies['H_BDCLCKID_SF'] = 'tJIqVIt2JKt3qRcFq4cqhRkthxJeanLXKKOLVh6VLPOkeq8CD4czKpjXDNJ3hxkH2Ncf3KOM3pv-JJc2y5jHhPFsM4cyWtbKbGOzVU-b3MopsIJMMxFWbT8U5fKDq4tfaKviaK5EBMb1MC5Me4bK-TrLDGKqtU5'
        temp_cookies['Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574'] = '1530773001'
        temp_cookies['BDORZ'] = 'B490B5EBF6F3CD402E515D22BCDA1598'
        temp_cookies['H_PS_PSSID'] = '1460_26431_21084_22159'
        temp_cookies['PSINO'] = '7'
        temp_cookies['MCITY'] = '-%3A'
        temp_cookies['BAIDUID'] = 'C6404371DAAB9403AA9476EF257D6BF6'
        temp_cookies['BIDUPSID'] = 'C6404371DAAB9403AA9476EF257D6BF6'
        result_cookies = ''
        for (k,v) in temp_cookies.items():
            result_cookies += '%s=%s; ' % (k,v)
        # result_cookies = 'from_lang_often=%s; to_lang_often=%s ' % (temp_cookies['from_lang_often'], temp_cookies['to_lang_often'],)
        self.headers['Cookie'] = result_cookies

        return self.data, self.headers['Cookie']

    def parse_cookies(self, cookies_temp):
        cookies = {}
        for line in cookies_temp:
            cookies[line['name']] = line['value']
        return cookies


baidu = BaiDuModel()
content = '我爱你'
data, cookies = baidu.parse_content(content)
print(data)
print(cookies)

response = requests.post(url='http://fanyi.baidu.com/v2transapi',data=data,headers=baidu.headers)
result = response.text
dict = json.loads(result)
try:
    print(dict['trans_result']['data'][0])
    print('原文 %s : 译文 %s' % (content, dict['trans_result']['data'][0]['dst']))
except KeyError:
    print('失败! 报文：%s' % dict)
