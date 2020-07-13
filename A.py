#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/9/26 11:30
# @Author: dqj

from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml import etree


# 爬取“部”
# part = soup.find_all('td', {'class': 'IPCContentRow'})
# for p in part:
#     print(p.get_text())

# 爬取“大类”
# mainCategory = soup.find_all('tr', {'class': 'IPCContentRow'})
# for m in mainCategory:
#     print(m.get_text())

# 爬取A部下的所有层次分类
# def crawl(beautifulsoup, ipchtml):
#     parts = beautifulsoup.find_all('tr', {'class': 'IPCContentRow'})
#     for p in parts:
#         print(p.get_text())
#         ipcchild = p.find('td', {'class': 'IPCChild'})
#         result = ipchtml.xpath('')
#         while ipcchild.find('a'):
#             a = ipcchild.find('a')
#             innerhtml = urlopen(a['href']).read().decode('uft-8')
#             innersoup = BeautifulSoup(innerhtml, features='lxml')
#             crawl(innersoup, innerhtml)


# if has Chinese, apply decode()
html = urlopen("http://www.soopat.com/IPC/Parent/A").read()
# 构造一个XPath解析对象
selector = etree.HTML(html)
links = selector.xpath('//*[@class="IPCContentRow"]/td[2]/a[@href]')
for link in links:
    print(link)
# soup = BeautifulSoup(html, features='lxml')
