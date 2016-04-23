腾讯招聘爬虫(2016/4/18)
========= 
##第一步(先获取招聘的最大页数)
```Python
def getMaxPageNum():
    hrUrl = 'http://hr.tencent.com/position.php'
    pageData = sess.get(hrUrl).content.decode()
    soup = BeautifulSoup(pageData,'html.parser')
    maxPageNum = int(soup.find('div',class_='pagenav').contents[-3].string)
    return maxPageNum
```

##第二步(获取所有工作的基本信息)
```Python
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
```

##第三步(获取一个工作的职责和要求)
```Python
def getJobInfo(jobUrl):
    jobUrl = "http://hr.tencent.com/%s" %jobUrl
    pageData = sess.get(jobUrl).content.decode()
    
    soup = BeautifulSoup(pageData,'html.parser')
    jobDuty,jobAsk = soup.find_all('ul',class_='squareli')
    
    dutyStrList = list((li.string for li in jobDuty.find_all('li')))
    askStrList = list((li.string for li in jobAsk.find_all('li')))
    jobInfo = {"duty":dutyStrList,"ask":askStrList}

    return jobInfo
```

***具体的请看spider.py中的代码*