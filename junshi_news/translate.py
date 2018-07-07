# -*-coding=utf-8-*-

from junshi_news.lib.google import GoogleModel
from junshi_news.lib.baidut import BaiduModel
from urllib import parse
import execjs
import requests
import re

from selenium import webdriver
ctx = execjs.compile("""
        function a(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}var C=null;var hash=function(r,_gtk){var o=r.length;o>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(o/2)-5,10)+r.substr(-10,10));var t=void 0,t=null!==C?C:(C=_gtk||"")||"";for(var e=t.split("."),h=Number(e[0])||0,i=Number(e[1])||0,d=[],f=0,g=0;g<r.length;g++){var m=r.charCodeAt(g);128>m?d[f++]=m:(2048>m?d[f++]=m>>6|192:(55296===(64512&m)&&g+1<r.length&&56320===(64512&r.charCodeAt(g+1))?(m=65536+((1023&m)<<10)+(1023&r.charCodeAt(++g)),d[f++]=m>>18|240,d[f++]=m>>12&63|128):d[f++]=m>>12|224,d[f++]=m>>6&63|128),d[f++]=63&m|128)}for(var S=h,u="+-a^+6",l="+-3^+b+-f",s=0;s<d.length;s++)S+=d[s],S=a(S,u);return S=a(S,l),S^=i,0>S&&(S=(2147483647&S)+2147483648),S%=1e6,S.toString()+"."+(S^h)}
        """)
response = requests.get('http://fanyi.baidu.com/')
html = response.text
print(html)
content = '不要忘了我'
sign = re.findall(r'window.gtk = \'(.*)\'', html)[0]
token = re.findall(r'token: \'(.*)\'', html)[0]
sign = ctx.call('hash', content, sign)
url = 'http://fanyi.baidu.com/v2transapi?from=zh&to=en&query=' + parse.quote(content) \
      + '&transtype=translang&simple_means_flag=3&sign=' + sign + '&token=' + token
print("gtk = " + sign)
print("token = " + token)

cookie1 = """PSTM=1525577599; BAIDUID=C06332363CA1FD2AE912122974920508:FG=1; BIDUPSID=50EF426E764EA45414E51BADF5D59967; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=VpveVR1Z342WW5nQmJ5bTZ0RDQwU3hjVWxmNmZ-U09iMVBIMHFTRHB3N1dTVlZiQUFBQUFBJCQAAAAAAAAAAAEAAADnz7y70tTRzLT6yrO05MO3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANa8LVvWvC1bY; H_WISE_SIDS=124304_123798_123335_120131_118895_118870_118839_118825_118797_122440_107318_117436_122789_124069_124396_123984_124110_123814_123956_123812_123852_123747_123980_124080_124030_110085_123290_100458; H_PS_PSSID=1451_21126_26350_22158; BDSFRCVID=nYAsJeC62CkuyZn7b1CrhVwc3g2rLfvTH6aIFqeyu4OI02iZhkonEG0PDU8g0Kub-RSSogKK5mOTH65P; H_BDCLCKID_SF=tJIDoIL2JC_3qn5zqROHhRIJhpo-KnLXKKOLVMTs2-Okeq8CDxQxKxtrjNtHLR8ObI6T2hn2K-T_8IO2y5jHhpkNDROBKqc82DT7Qbrt0-bpsIJMM4DWbT8ULfKL2lOzaKviaK8-BMb1MC5Me6KMj5JLDNtDq-JQ2C7WQb5-bJK_ebj45bbq-JDSM2TXKR0sKGQmQhcH0KLKEPoyblK-jP_HQP-O2tJZQT-JBnCMJxb1MRjVQqno-JIA-UJCbhb2ynnW0l5TtUJUeCnTDMRh-xuZMn3yKMniWKj9-pPhaMt0hC-mDTL5jToM-Uv05-ne56rq06reK4oMqn5pK4bsq4C85aRgJJQeWDTm_Don-fntVCL6-tTjLn0_0-n7Kj33aR4t-pPKKlTNHpctQx5PXh00hfbvtPn-3mkjbpbDfn02OP5PXqjO0-4syP4eJfRnWnFtbIF-JCDKMDKRjTRb5nbH2x705t4XbTFsWfTp-hcqEIL4LPRh2qIHjUKD3bj3Qjv2ob0--qRtfxbSj4QzQR_82q_JWMFjtD5zBnvOaq5nhMJe3j7JDMP0-mcNQhJy523i_R6vQpP-Mftu-n5jHjjXDarP; PSINO=7; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1530520843,1530522795,1530526620,1530534995; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1530534995; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D"""
def stringToDict(cookie):
    '''
    将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
    :return:
    '''
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict


cookie = stringToDict(cookie1)
headers = {
'Host': 'fanyi.baidu.com',
'Connection': 'keep-alive',
'Content-Length': '188',
'Accept': '*/*',
'Origin': 'http://fanyi.baidu.com',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': 'http://fanyi.baidu.com/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'cookie':cookie1
}
print(headers)
data = {'from': 'zh','to': 'en','query': content,'transtype': 'realtime','simple_means_flag': '3','sign': '901565.598668','token': '32fa829572a460df61eb23d04261f2e6'}

# sug = requests.post('http://fanyi.baidu.com/sug',headers=headers).text
# langdetect = requests.post('http://fanyi.baidu.com/langdetect',data={'query':'我'},headers=headers).text
sug = ''
langdetect = ''
message = requests.post('http://fanyi.baidu.com/v2transapi',data=data,headers=headers).text
print("sug = %s \nlangdetect = %s \nmessage = %s" % (sug,langdetect,message))



