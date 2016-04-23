#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- author: Wd0g  -*-

import requests,re
from bs4 import BeautifulSoup

sess = requests.Session()
def getMaxPageNum():
    pageData = sess.get("http://www.mp4ba.com").content.decode()
    soup = BeautifulSoup(pageData,'html.parser')
    pageNum = int(soup.find_all("a",class_="pager-last active")[0].string)
    return pageNum

def getMp4List(page):
    pageData = sess.get("http://www.mp4ba.com/index.php?page=%d" %page).content.decode()
    soup = BeautifulSoup(pageData,'html.parser')
    infoList = soup.find_all("tr",class_='alt1')
    infoLen = 0
    mp4InfoList = []
    for info in infoList:
        infoLen += 1
        try:
            date,categroy,title_url,size,seed,download,ok,*infoList = info.find_all('td')
        except Exception as e:
            pass
        finally:
            title = title_url.a.string.string.replace("\n",'').replace(" ",'').replace("\r",'')
            mp4Url= title_url.a['href']
            mp4Info = {"时间":date.string,"分类":categroy.string,"标题":title,"地址":mp4Url,"文件大小:":size.string,
                       "种子":seed.contents[1].string,"下载量":download.contents[1].string,
                       "下载完成":ok.contents[1].string,}
            mp4InfoList.append(mp4Info)

    infoList = soup.find_all('tr',class_='alt2')
    for info in infoList:
        infoLen += 1
        try:
            date, categroy, title_url, size, seed, download, ok, *infoList = info.find_all('td')
        except Exception as e:
            pass
        finally:
            title = title_url.a.string.string.replace("\n", '').replace(" ", '').replace("\r", '')
            mp4Url = title_url.a['href']
            mp4Info = {"时间": date.string, "分类": categroy.string, "标题": title, "地址": mp4Url,
                        "种子": seed.contents[1].string, "下载量": download.contents[1].string,
                        "下载完成": ok.contents[1].string,}
            mp4InfoList.append(mp4Info)
    return mp4InfoList

def getSeed(mp4Url):
    mp4Url = "http://www.mp4ba.com/%s" % mp4Url
    pageData = sess.get(mp4Url).content.decode()
    soup = BeautifulSoup(pageData,'html.parser')
    magnet = soup.find('a',{"id":"magnet"})['href']
    return magnet

maxPageNum = getMaxPageNum() + 1
mp4InfoList = []

for page in range(0,maxPageNum):
    mp4Info = getMp4List(page)
    mp4InfoList += mp4Info
    print("页数:%d    MP4数量:%d" %(page,len(mp4Info)))
print("爬取电影列表完毕,总爬取数:%d\n现在开始爬取电影种子" %len(mp4InfoList))

for mp4Info in mp4InfoList:
    print(mp4Info['标题'])
    magnet = getSeed(mp4Info['地址'])

    print(magnet)
    mp4Info['种子地址'] = magnet

print(mp4InfoList)