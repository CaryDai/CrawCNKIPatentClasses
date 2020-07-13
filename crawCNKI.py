#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/6/17 15:54
# @Author: dqj

import urllib.request
from urllib import parse
import gzip
from lxml import etree
import pymysql
from seleniumrequests import Chrome


def crawCategories():
    url = 'https://kns8.cnki.net/kns/AdvSearch?dbprefix=SCDB&&crossDbcodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCYFD%2CSCOD%2CCISD%2CSNAD%2CBDZK%2CGXDB_SECTION%2CCJFN%2CCCJD'
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    # print(text)   # 得到网页源代码
    html = etree.HTML(text)  # 构造一个XPath解析对象并对HTML文本进行自动修正
    # result = etree.tostring(html).decode('utf-8')
    # print(result)
    top_ul = html.xpath('//ul[@class="nav-content-list"]/li')     # 第一次解析（解析返回的都是list）
    count = 0
    for top_li in top_ul:
        # print(etree.tostring(top_li))
        name = top_li.xpath('div/a/text()')
        code = top_li.xpath('div/@name')    # 获取属性值，因为分类代码在属性中指明
        parent_code = ''
        subject = Subject(name, code, parent_code)
        print(name, code)
        subTags = top_li.xpath('div//i')    # 获得div节点下的所有i节点，如果当前分类还有子分类的话(i标签个数为2)，则需要点击
        if len(subTags) == 2:
            count += 1
    print(count)


def crawSubjectCodes(parentId, naviItemlevel, db):
    """
    爬取知网分类名
    :param parentId:
    :param naviItemlevel:
    :param db:
    :return:
    """
    url = 'https://kns8.cnki.net/kns/AdvSearch/_GetAdvNavi'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'kns8.cnki.net',
        'Origin': 'https://kns8.cnki.net',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'dbcode': 'SCDB',
        'naviClassId': 'defult',
        'parentId': parentId,
        'naviItemlevel': naviItemlevel
    }
    data = parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url=url, data=data, headers=headers)
    resp = urllib.request.urlopen(req).read()
    # print(type(resp))   # <class 'bytes'>
    resp = gzip.decompress(resp).decode('utf-8')    # 服务器传过来的是压缩数据，利用gzip进行解压缩
    # print(resp)
    html = etree.HTML(resp)     # 构造成一个XPath解析对象
    list_li = html.xpath('//li')    # 得到返回页面中所有的li标签
    for li in list_li:
        name = li.xpath('div/a/text()')
        code = li.xpath('div/@name')
        parent_code = parentId
        level = naviItemlevel + 1
        sql = "INSERT INTO information_tech(class_name, class_code, parent_code, item_level) " \
              "VALUES ('%s','%s','%s','%s')"%(name[0], code[0], parent_code, level)
        db.cursor.execute(sql)
        db.conn.commit()
        # subject = Subject(name, code, parent_code, level)
        subTags = li.xpath('div//i')
        print(name, code, level)
        # i标签个数为2，说明还有下一级的分类
        if len(subTags) == 2:
            newParentId = code[0]
            newNaviItemlevel = naviItemlevel + 1
            crawSubjectCodes(newParentId, newNaviItemlevel, db)


def connectMysql():
    # 打开数据库连接
    conn = pymysql.connect("localhost", "root", "root", "class_codes")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    sqlConn = SqlConn(conn, cursor)
    return sqlConn


class SqlConn:
    """
    mysql连接类
    """
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor


class Subject:
    """
    学科类
    __init__()方法是一种特殊的方法，被称为类的构造函数或初始化方法，当创建了这个类的实例时就会调用该方法
    self 代表类的实例，self 在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数。
    """

    def __init__(self, name, code, parent_code, level):
        self.name = name
        self.code = code
        self.parent_code = parent_code
        self.level = level


if __name__ == '__main__':
    # crawCategories()
    db = connectMysql()
    crawSubjectCodes('I', 1, db)
    db.cursor.close()
    db.conn.close()
