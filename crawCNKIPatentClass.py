#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/7/2 9:31
# @Author: dqj


import urllib.request
from urllib import parse
import gzip
from lxml import etree
import pymysql
from crawCNKI import SqlConn


def crawIPC(patentCode, naviItemlevel, db):
    url = 'https://kns.cnki.net/kns/request/NaviGroup.aspx?code=' + patentCode + \
          '&tpinavigroup=SCPD_FMtpiresult&catalogName=SCPD_IPCCLS&__=Thu%20Jul%2002%202020%2010%3A18%3A19%20GMT' \
          '%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4) '
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'kns.cnki.net',
        'Referer': 'https://kns.cnki.net/kns/brief/result.aspx?dbPrefix=SCPD_FM',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
    }
    data = {
        'code': patentCode,
        'tpinavigroup': 'SCPD_FMtpiresult',
        'catalogName': 'SCPD_IPCCLS'
    }
    data = parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url=url, data=data, headers=headers)
    resp = urllib.request.urlopen(req).read()
    resp = gzip.decompress(resp).decode('utf-8')  # 服务器传过来的是压缩数据，利用gzip进行解压缩
    # print(resp)
    html = etree.HTML(resp)  # 构造成一个XPath解析对象
    list_dd = html.xpath('//dd')
    i = 0
    for dd in list_dd:
        i += 1
        name = dd.xpath('a/text()')
        code = dd.xpath('span/input[@id="selectbox"]/@value')
        parent_code = patentCode
        level = naviItemlevel + 1
        print(name, code, level)
        sql = "INSERT INTO ipc_h(ipc_name, ipc_code, parent_code, item_level) " \
              "VALUES ('%s','%s','%s','%s')" % (name[0], code[0], parent_code, level)
        db.cursor.execute(sql)
        db.conn.commit()
        # 获取当前dd标签的下一个标签，如果下一个是dl标签，说明它还有子类
        nextLabel = html.xpath('//dd[' + str(i) + ']/following-sibling::*[1]')
        blabel = etree.tostring(nextLabel[0])   # bytes
        slabel = str(blabel, encoding="utf-8")  # 转成str
        if slabel.find("dl") == 1:
            newPatentCode = code[0]
            newNaviItemlevel = naviItemlevel + 1
            crawIPC(newPatentCode, newNaviItemlevel, db)


def connectMysql():
    # 打开数据库连接
    conn = pymysql.connect("localhost", "root", "root", "class_codes")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    sqlConn = SqlConn(conn, cursor)
    return sqlConn


if __name__ == '__main__':
    db = connectMysql()
    crawIPC('H', 1, db)
    db.cursor.close()
    db.conn.close()
