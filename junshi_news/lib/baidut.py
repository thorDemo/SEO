import execjs
import re
import urllib.parse
from urllib import request
from http import cookiejar
import subprocess
import sqlite3
import requests



SOUR_COOKIE_FILENAME = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Cookies'
DIST_COOKIE_FILENAME = '.\python-chrome-cookies'


class BaiduModel:
    def __init__(self):
        self.result = ''
        self.ctx = execjs.compile("""
        function a(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}var C=null;var hash=function(r,_gtk){var o=r.length;o>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(o/2)-5,10)+r.substr(-10,10));var t=void 0,t=null!==C?C:(C=_gtk||"")||"";for(var e=t.split("."),h=Number(e[0])||0,i=Number(e[1])||0,d=[],f=0,g=0;g<r.length;g++){var m=r.charCodeAt(g);128>m?d[f++]=m:(2048>m?d[f++]=m>>6|192:(55296===(64512&m)&&g+1<r.length&&56320===(64512&r.charCodeAt(g+1))?(m=65536+((1023&m)<<10)+(1023&r.charCodeAt(++g)),d[f++]=m>>18|240,d[f++]=m>>12&63|128):d[f++]=m>>12|224,d[f++]=m>>6&63|128),d[f++]=63&m|128)}for(var S=h,u="+-a^+6",l="+-3^+b+-f",s=0;s<d.length;s++)S+=d[s],S=a(S,u);return S=a(S,l),S^=i,0>S&&(S=(2147483647&S)+2147483648),S%=1e6,S.toString()+"."+(S^h)}  
        """)

    # http://fanyi.baidu.com/v2transapi?from=zh&to=en&query=''&transtype=translang&simple_means_flag=3&sign=719145.924184&token=3a1ae6d96bdd2a8e0f2eb367cb23cb83
    #
    # 作者：HONGQUAN
    # 链接：https://www.jianshu.com/p/38a65d8d3e80
    # 來源：简书
    def translate(self, content):
        DOMAIN_NAME = '.baidu.com'
        get_url = r'http://fanyi.baidu.com/'
        rq = requests.get('http://fanyi.baidu.com/')
        print(rq.cookies.get_dict())
        # headers = {'Cookie': rq.cookies}

        response = requests.get(get_url)
        html = response.read().decode('utf-8')

        sign = re.findall(r'window.gtk = \'(.*)\'', html)[0]
        token = re.findall(r'token: \'(.*)\'', html)[0]
        sign = self.ctx.call('hash', content, sign)
        url = 'http://fanyi.baidu.com/v2transapi?from=zh&to=en&query=' + urllib.parse.quote(content)\
              + '&transtype=translang&simple_means_flag=3&sign=' + sign + '&token=' + token
        print("gtk = " + sign)
        print("token = " + token)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        print(response.read().decode('utf-8'))
        return html

    def get_chrome_cookies(self, url):
        cookie = cookiejar.CookieJar()
        # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
        handler = request.HTTPCookieProcessor(cookie)
        # 通过CookieHandler创建opener
        opener = request.build_opener(handler)
        # 此处的open方法打开网页
        response = opener.open('http://www.baidu.com')
        # 打印cookie信息
        for item in cookie:
            print('Name = %s' % item.name)
            print('Value = %s' % item.value)
        return cookie



