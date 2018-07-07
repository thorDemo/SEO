import scrapy
from scrapy.http import Request,FormRequest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import re
import execjs
from urllib import parse
from scrapy.http.cookies import CookieJar
import time
import requests


class TranslateSpider(scrapy.Spider):

    name = 'translatespider'

    ctx = execjs.compile("""
            function a(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}var C=null;var hash=function(r,_gtk){var o=r.length;o>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(o/2)-5,10)+r.substr(-10,10));var t=void 0,t=null!==C?C:(C=_gtk||"")||"";for(var e=t.split("."),h=Number(e[0])||0,i=Number(e[1])||0,d=[],f=0,g=0;g<r.length;g++){var m=r.charCodeAt(g);128>m?d[f++]=m:(2048>m?d[f++]=m>>6|192:(55296===(64512&m)&&g+1<r.length&&56320===(64512&r.charCodeAt(g+1))?(m=65536+((1023&m)<<10)+(1023&r.charCodeAt(++g)),d[f++]=m>>18|240,d[f++]=m>>12&63|128):d[f++]=m>>12|224,d[f++]=m>>6&63|128),d[f++]=63&m|128)}for(var S=h,u="+-a^+6",l="+-3^+b+-f",s=0;s<d.length;s++)S+=d[s],S=a(S,u);return S=a(S,l),S^=i,0>S&&(S=(2147483647&S)+2147483648),S%=1e6,S.toString()+"."+(S^h)}  
            """)
    start_urls = ['http://fanyi.baidu.com']

    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'keep-alive',
        'Content-Length':'116',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'fanyi.baidu.com',
        'Origin':'http://fanyi.baidu.com',
        'Referer':'http://fanyi.baidu.com/',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
        'Cookie':'locale=zh; BAIDUID=20C8A872A70FCDC54614070B00FD372F:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1530762350; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1530762374'
    }

    def parse(self, response):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        prefs = {'profile.managed_default_content_settings.images': 2, 'profile.default_content_settings.popups': 0}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        content = '我的'
        driver.get('http://fanyi.baidu.com')
        cookies = self.parse_cookies(driver.get_cookies())
        html = driver.execute_script("return document.documentElement.outerHTML")
        driver.close()
        gtk = re.findall(r'window.gtk = \'(.*)\'', html)[0]
        token = re.findall(r'token: \'(.*)\'', html)[0]
        sign = self.ctx.call('hash', content, gtk)

        url = 'http://fanyi.baidu.com/v2transapi?from=zh&to=en&query=' + parse.quote(content) \
              + '&transtype=translang&simple_means_flag=3&sign=' + sign + '&token=' + token
        print("gtk = " + sign)
        print("token = " + token)
        result = requests.post(url,headers=self.headers)
        print(result)
        # yield Request(url=url, headers=self.headers, callback=self.next)

    def next(self, response):
        html = response.body.decode("utf-8")
        print(html)
        time.sleep(60)

    def parse_cookies(self, cookies_temp):
        cookies = {}
        for line in cookies_temp:
            name = line['name']
            value = line['value']
            cookies[name] = value
        print(cookies)
        return cookies