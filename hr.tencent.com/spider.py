#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- author: Wd0g  -*-

import requests,re
from bs4 import BeautifulSoup

#: 获取最大页数
def getMaxPageNum():
    hrUrl = 'http://hr.tencent.com/position.php'
    pageData = sess.get(hrUrl).content.decode()
    soup = BeautifulSoup(pageData,'html.parser')
    maxPageNum = int(soup.find('div',class_='pagenav').contents[-3].string)
    return maxPageNum

#: 获取所有工作的基本信息
def getJobList(pageNum):
    jobUrl = 'http://hr.tencent.com/position.php?&start=%d#a' %pageNum
    jobList = []

    pageData = sess.get(jobUrl).content.decode()
    soup = BeautifulSoup(pageData,'html.parser')
    _,*jobInfoList,_ = soup.find('table',class_='tablelist').find_all('tr')

    for jobInfo in jobInfoList:
        title_url_Td,*infoTd = jobInfo.find_all('td')
        jobInfo = {'title':title_url_Td.a.string,
                   'jobUrl':title_url_Td.a['href'],
                   'categroy':infoTd[0].string,
                   'needNum':infoTd[1].string,
                   'address':infoTd[2].string,
                   'date':infoTd[3].string,
                   'other':[]}
        jobList.append(jobInfo)

    return jobList

#: 获取一个工作的职责和要求
def getJobInfo(jobUrl):
    jobUrl = "http://hr.tencent.com/%s" %jobUrl
    pageData = sess.get(jobUrl).content.decode()

    soup = BeautifulSoup(pageData,'html.parser')
    jobDuty,jobAsk = soup.find_all('ul',class_='squareli')

    dutyStrList = list((li.string for li in jobDuty.find_all('li')))
    askStrList = list((li.string for li in jobAsk.find_all('li')))
    jobInfo = {"duty":dutyStrList,"ask":askStrList}

    return jobInfo

#>>0:初始化一些变量
sess = requests.Session()
maxPageNUm = getMaxPageNum()
jobs = []

#>>1:爬取所有工作
for pageNum in range(0,maxPageNUm,10):
    print(pageNum)
    jobList = getJobList(pageNum)
    jobs += jobList

#>>2:爬取所有工作的要求和职责
for jobInfo in jobs:
    jobInfo['other']= getJobInfo(jobInfo['jobUrl'])

print(jobs)
