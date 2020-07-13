#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/6/14 21:36
# @Author: dqj

import requests  # 导入requests包
from bs4 import BeautifulSoup
import re

url = 'http://www.cntour.cn/'
strhtml = requests.get(url)  # Get方式获取网页数据
# print(strhtml.text)
soup = BeautifulSoup(strhtml.text, 'lxml')
data = soup.select('#main>div>div.mtop.firstMod.clearfix>div.centerBox>ul.newsList>li>a')
print(data)
for item in data:
    result = {
        'title': item.get_text(),  # 标题在<a>标签中，提取标签的正文用 get_text() 方法
        'link': item.get('href'),  # 提取标签中的 href 属性用 get() 方法，在括号中指定要提取的属性数据，即 get('href')
        'ID': re.findall('\d+', item.get('href'))   # 第一个参数表示正则表达式，第二个参数表示要提取的文本。
    }
print(result)

# def get_translate_date(word=None):
#     url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
#     From_data = {'i': word, 'from': 'AUTO', 'to': 'AUTO', 'smartresult': 'dict', 'client': 'fanyideskweb',
#                  'salt': '15922704887949', 'sign': '0b338f88e43f50f9c838c8dd6db30597', 'ts': '1592270488794',
#                  'bv': 'd17d9dd026a611df0315b4863363408c', 'doctype': 'json', 'version': '2.1', 'keyfrom': 'fanyi.web',
#                  'action': 'FY_BY_REALTIME'}
#     # 请求表单数据
#     response = requests.post(url, data=From_data)
#     # 将Json格式字符串转字典
#     content = json.loads(response.text)
#     print(content)
#     # 打印翻译后的数据
#     # print(content['translateResult'][0][0]['tgt'])
#
#
# if __name__ == '__main__':
#     get_translate_date('我爱中国')
