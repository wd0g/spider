#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- author: Wd0g  -*-

import requests,threading,time
from colorama import init,Fore

#获取进度条文本
def getProgress(current,max):
    max -= 1
    a = max / 100
    b = current /a
    bfs = (current / max) * 100
    maxStr = "-" * int(100 - b)
    currentStr = "="* int(b)
    return "[%s%s](%.2f%s)" %(currentStr,maxStr,bfs,'%')
#获取当前时间文本
def getStrTime():
    timeStr = Fore.GREEN + time.strftime("%m-%d %H:%M:%S",time.localtime())+Fore.WHITE
    return "[%s] " %timeStr
#输出彩色字体
def echo(data,level):
    dataStr = getStrTime()
    if level == 1:#正常输出
        dataStr += Fore.LIGHTCYAN_EX+"[+] " +Fore.LIGHTCYAN_EX + data + " "*50
    elif level == 2:#成功输出
        dataStr += Fore.LIGHTGREEN_EX + "[!] " + Fore.LIGHTGREEN_EX + data + " "*50
    elif level == 3:#失败输出
        dataStr += Fore.LIGHTRED_EX + "[*] " + Fore.LIGHTRED_EX + data + " "*50
    print(dataStr+Fore.WHITE)
#创建网站数组
def mkUrlList(maxNum):
    urlList = list(("http://zone.wooyun.org/content/%d" %num for num in range(0,maxNum)))
    return urlList
#判断是否为帖子
def isPage(url):
    try:
        res = requests.Session().get(url)
        pageData = res.content.decode()
    except:
        return False

    if pageData.find("<title>登录 -- WooYun(白帽子技术社区)</title>") != -1:
        return False
    else:
        return pageData
#保存帖子
def savePage(pageId,pageData):
    file = open("./page/%d.html" % pageId, 'w', encoding="utf-8")
    file.write(pageData)
    file.close()
#开始
def action():
    global urlId
    bool = True
    while bool:
        try:
            threadLock.acquire()
            id = urlId
            url = urlList[id]
            urlId += 1
        except:
            bool = False
            return
        threadLock.release()

        pageData = isPage(url)
        threadLock.acquire()
        if pageData:
            savePage(id,pageData)
            echo("[帖子]%s" %url,2)
        else:
            echo("[登录]%s" %url,3)
        threadLock.release()
        print(getProgress(id, len(urlList)), end='\r')

init(wrap=True)                #windows系统为True,linux系统为False(输出颜色)
urlId   = 0                     #标识当前要读取的URL
urlList = mkUrlList(80000)      #创建5000个URL
thread  = 30                    #线程数20
threadLock = threading.Lock()   #线程锁
threadList = []                 #线程数组

for i in range(0,thread):
    t = threading.Thread(target=action)
    t.setDaemon(True)
    threadList.append(t)
for t in threadList:
    t.start()
for t in threadList:
    t.join()