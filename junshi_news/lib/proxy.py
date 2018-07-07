# -*-coding=utf-8-*-
from urllib import request
import random
import json


if __name__ == "__main__":
    # 访问网址
    url = 'http://47.96.139.87:8081/Index-generate_api_url.html?packid=7&fa=5&qty=5&port=1&format=json&ss=5&css=&ipport=1&et=1&pro=&city='
    response = request.urlopen(url)
    result = response.read().decode("utf-8")
    rs = json.load(result)
    print(rs['data'])

