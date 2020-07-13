#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/6/16 10:04
# @Author: dqj

import requests  # 导入requests包
from bs4 import BeautifulSoup
import urllib.request
from lxml import etree


def crawSubjects():
    url = 'http://www.letpub.com.cn/index.php?page=dict&level1=allfields'
    resp = urllib.request.urlopen(url)
    html = resp.read()
    selector = etree.HTML(html)
    subjects = selector.xpath("/html/body/div[4]/div/div[2]/div[2]/div[@class='subject']/a/text()")
    print(subjects)

    # url = 'http://www.letpub.com.cn/index.php?page=dict&level1=allfields'
    # html = requests.get(url)
    # soup = BeautifulSoup(html.text, 'lxml')
    # data = soup.select('#dict > div:nth-child(2)')
    # for item in data:
    #     result = {
    #         'subtitle': item.get_text()
    #     }
    #     print(result)


if __name__ == '__main__':
    crawSubjects()
