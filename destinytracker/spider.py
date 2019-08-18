import requests
import requests.exceptions
import threadpool
import os
from bs4 import BeautifulSoup
import hashlib
import json
import csv
import time
import re
import threading
import winsound

firstReferer = 'https://destinytracker.com/d2/profile/psn/Kyle_lks'

headers = {
    "Accept": "application/json, text/plain, */*",
    'cookie':'__cfduid=dfe5b67eff914687e66c961048e0b351c1566095116; X-Mapping-Server=s4; _ga=GA1.2.48801697.1566095141; _gid=GA1.2.1561335858.1566095141; __gads=ID=7eb18feca09b8ec9:T=1566095143:S=ALNI_MZSKhrqjBMgatScmQbC6vsDXQ03eQ; UserName=Guest66; __ControllerTempData=AAEAAAD/////AQAAAAAAAAAEAQAAAOIBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuRGljdGlvbmFyeWAyW1tTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uT2JqZWN0LCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQMAAAAHVmVyc2lvbghDb21wYXJlcghIYXNoU2l6ZQADAAgWU3lzdGVtLk9yZGluYWxDb21wYXJlcggAAAAACQIAAAAAAAAABAIAAAAWU3lzdGVtLk9yZGluYWxDb21wYXJlcgEAAAALX2lnbm9yZUNhc2UAAQEL',
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    'X-Requested-With':'XMLHttpRequest',
    'Referer':firstReferer,
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36'
}
innoHeaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'cookie':'__cfduid=dfe5b67eff914687e66c961048e0b351c1566095116; X-Mapping-Server=s4; _ga=GA1.2.48801697.1566095141; _gid=GA1.2.1561335858.1566095141; __gads=ID=7eb18feca09b8ec9:T=1566095143:S=ALNI_MZSKhrqjBMgatScmQbC6vsDXQ03eQ; UserName=Guest66; __ControllerTempData=AAEAAAD/////AQAAAAAAAAAEAQAAAOIBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuRGljdGlvbmFyeWAyW1tTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uT2JqZWN0LCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQMAAAAHVmVyc2lvbghDb21wYXJlcghIYXNoU2l6ZQADAAgWU3lzdGVtLk9yZGluYWxDb21wYXJlcggAAAAACQIAAAAAAAAABAIAAAAWU3lzdGVtLk9yZGluYWxDb21wYXJlcgEAAAALX2lnbm9yZUNhc2UAAQEL',
    'Referer':'https://destinytracker.com/d2/leaderboards',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36'
}

lock = threading.Lock()
reqNum = 0
threadNum = 1
req = requests.session()
req.headers = headers

savePath = "输出"
if not os.path.exists(savePath):
    os.makedirs(savePath)
colNum = 0

csvFile = open("{}/玩家游戏信息.csv".format(savePath), mode="w", encoding="gbk",
                   newline="")
csvWriter = csv.writer(csvFile)
titleBar = ['pid','name','period', 'assists', 'score', 'kills', 'averageScorePerKill', 'deaths', 'averageScorePerLife', 'completed', 'opponentsDefeated', 'efficiency', 'killsDeathsRatio', 'killsDeathsAssists', 'activityDurationSeconds', 'standing', 'team', 'completionReason', 'fireteamId', 'startSeconds', 'timePlayedSeconds', 'playerCount', 'teamScore']
csvWriter.writerow(titleBar)
csvFile.close()

csvFile = open("{}/玩家基本信息.csv".format(savePath), mode="w", encoding="gbk",
                   newline="")
csvWriter = csv.writer(csvFile)
titleBar = ['pid', 'name', 'casual-KD', 'casual-KDA', 'casual-KA/d', 'casual-Win%', 'casual-Glory Rating', 'casual-Glory Level', 'casual-Valor Rating', 'casual-Valor Level', 'casual-Infamy Rating', 'casual-Infamy Level', 'casual-Matches', 'casual-Wins', 'casual-Losses', 'casual-Flawless Cards', 'casual-Site Score', 'casual-Ability Kills', 'casual-Assists', 'casual-Assists Pga', 'casual-Total Kill Distance', 'casual-Kills', 'casual-Kills Pga', 'casual-Avg Kill Distance', 'casual-Deaths', 'casual-Average Life Span', 'casual-Score', 'casual-Score Pga', 'casual-Avg Score Per Kill', 'casual-Avg Score Per Life', 'casual-Best Single Game Kills', 'casual-Best Single Game Score', 'casual-Objectives Completed', 'casual-Suicides', 'casual-Time Played', 'casual-Super Kills', 'overall-KD', 'overall-KDA', 'overall-KA/d', 'overall-Win%', 'overall-Glory Rating', 'overall-Glory Level', 'overall-Valor Rating', 'overall-Valor Level', 'overall-Infamy Rating', 'overall-Infamy Level', 'overall-Matches', 'overall-Wins', 'overall-Losses', 'overall-Flawless Cards', 'overall-Site Score', 'overall-Ability Kills', 'overall-Assists', 'overall-Assists Pga', 'overall-Total Kill Distance', 'overall-Kills', 'overall-Kills Pga', 'overall-Avg Kill Distance', 'overall-Deaths', 'overall-Average Life Span', 'overall-Score', 'overall-Score Pga', 'overall-Avg Score Per Kill', 'overall-Avg Score Per Life', 'overall-Best Single Game Kills', 'overall-Best Single Game Score', 'overall-Objectives Completed', 'overall-Suicides', 'overall-Time Played', 'overall-Super Kills']
csvWriter.writerow(titleBar)
csvFile.close()

def retry(count=1):
    def dec(f):
        def ff(*args, **kwargs):
            ex = None
            for i in range(count):
                try:
                    ans = f(*args, **kwargs)
                    return ans
                except Exception as e:
                    ex = e
            raise ex

        return ff

    return dec

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@retry(20)
def postApi(url,data):
    global req
    global reqNum
    reqNum +=1
    # print("程序第",reqNum,"次请求~")
    # 请求模块执行POST请求,response为返回对象

    try:
        response = req.post(url, data=data,timeout=5)
    except requests.exceptions.ConnectTimeout:
        getIp()


    # 从请求对象中拿到相应内容解码成utf-8 格式
    html = response.content.decode("utf-8")
    return html
@retry(10)
def loadPage(url,srb = False):
    global req
    global reqNum
    reqNum +=1
    # print("程序第",reqNum,"次请求~")
    # 请求模块执行POST请求,response为返回对象
    response = req.get(url, timeout=10)
    if srb:
        return response.content
    # 从请求对象中拿到相应内容解码成utf-8 格式
    html = response.content.decode("utf-8")
    return html



def general():
    for i in range(1,10000):
        s = "0000{}".format(i)[-4:]
        yield "******"+s

def parser(rule):

    global req

    csvFile = open("{}/玩家基本信息.csv".format(savePath), mode="a", encoding="gbk",
                   newline="")
    csvWriter = csv.writer(csvFile)

    url = 'https://destinytracker.com/d2/search?name={}'.format(rule)
    
    req.headers = innoHeaders
    html = loadPage(url)
    req.headers = headers

    pidReg = re.compile('/(.*?)/recentgames').findall(html)
    if len(pidReg) !=0:
    	pid = pidReg[0].strip("d2/api/profile/2/")
    else:
    	print('miss')
    	return

    dataList = [pid,rule]

    playerDataReg = re.compile('var playerData = (.*?);</script>',re.S).findall(html)
    if len(playerDataReg)!=0:
    	playerData = json.loads(playerDataReg[0])
    	casual = playerData['casual']
    	for item in casual:
    		print(item['label'],item['displayValue'])
    		dataList.append(item['displayValue'])
    	overall = playerData['overall']
    	for item in overall:
    		print(item['label'],item['displayValue'])
    		dataList.append(item['displayValue'])
    else:
    	print('miss')
    csvWriter.writerow(dataList)
    csvFile.close()

    csvFile = open("{}/玩家游戏信息.csv".format(savePath), mode="a", encoding="gbk",
                   newline="")
    csvWriter = csv.writer(csvFile)
    url = "https://destinytracker.com/d2/api/profile/2/{}/recentgames?mode=5".format(pid)
    jsonText = loadPage(url)
    jsonData = json.loads(jsonText)
    matches = jsonData['matches']
    
    for matche in matches:
    	dataList = [pid,rule]
    	period = matche['period']
    	# print(period)
    	dataList.append(period)
    	values = matche['values']
    	for value in values:
    		# print("\t",value,values[value]['basic']['value'])
    		dataList.append(values[value]['basic']['value'])
    	csvWriter.writerow(dataList)
    csvFile.close()


@log("execute")
def func(rule=""):
    global colNum
    params = []
    
    params.append(([rule], None))

    taskPool = threadpool.ThreadPool(threadNum)
    spiders = threadpool.makeRequests(parser, params)

    for spider in spiders:
        taskPool.putRequest(spider)
    taskPool.wait()


def Main():
    sourceTxt = open("source.txt").read()
    keywordList = sourceTxt.split("\n")
    for keyword in keywordList:
       	func(keyword)



if __name__ == "__main__":
    Main()