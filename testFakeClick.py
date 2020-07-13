#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/6/22 11:08
# @Author: dqj


from selenium import webdriver
import time
import re

opt = webdriver.ChromeOptions()  # 创建浏览
# opt.set_headless()    #无窗口模式
driver = webdriver.Chrome(options=opt)  # 创建浏览器对象
driver.get('https://www.baidu.com/')  # 打开网页
# driver.maximize_window()   #最大化窗口
time.sleep(2)  # 加载等待
driver.find_element_by_xpath("//input[@id='kw']").send_keys("IPhone")  # 利用xpath查找元素进行输入文本

# driver.find_element_by_id('kw').send_keys("小米") #候选方法

driver.find_element_by_xpath("//span[@class='bg s_btn_wr']/input").click()  # 点击按钮

# driver.find_element_by_xpath("//input[@value='百度一下']").click()#候选方法

# driver.find_element_by_xpath("//span[@class='bg s_btn_wr']/input[type='submit'][value='百度一下']").click()#候选方法,多条件匹配
