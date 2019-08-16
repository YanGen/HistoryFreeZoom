import requests
import re
import csv
from bs4 import BeautifulSoup



indexList = [
    "https://www.phb123.com/mpv/",
    "https://www.phb123.com/suv/",
    "https://www.phb123.com/xcsuv/",
    "https://www.phb123.com/jcxsuv/",
    "https://www.phb123.com/zxsuv/",
    "https://www.phb123.com/zdxsuv/",
    "https://www.phb123.com/jincouche/",
    "https://www.phb123.com/zhongxingche/",
    "https://www.phb123.com/zdxc/",
    "https://www.phb123.com/xiaoxingche/",
    "https://www.phb123.com/weixingche/",
]

def crawlIndex():
    csvFile = open("data.csv", mode="w", encoding="gbk", newline="")
    csvWriter = csv.writer(csvFile)
    for index in indexList:
        response = requests.get(index)
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html,"html.parser")
        table = soup.find('table', attrs={'class': 'rank-table'})
        trTags = table.find_all("tr")[1:11]
        for trTag in trTags:
            tdTags = trTag.find_all("td")
            row = []
            for tdTag in tdTags:
                tdTxt = tdTag.get_text()
                aTag = tdTag.find("a")
                if aTag:
                    row.append("https://www.phb123.com/"+aTag['href'])
                if tdTxt:
                    row.append(tdTxt.replace("\n\n","").strip())
            del row[0],row[2]
            row += crawlDetail(row[0])
            row = [item.encode("gbk","ignore").decode("gbk") for item in row]
            print(row)
            csvWriter.writerow(row)

    csvFile.close()


def crawlDetail(url):
    response = requests.get(url)
    html = response.content.decode("utf-8")
    pailiangReg = re.compile('<li>排量：<span>(.*?)</span></li>').findall(html)
    if len(pailiangReg) != 0:
        pailiang = pailiangReg[0]
    else:
        pailiang = ""
    youhaoReg = re.compile('<li>油耗：<span>(.*?)</span></li>').findall(html)
    if len(youhaoReg) != 0:
        youhao = youhaoReg[0]
    else:
        youhao = ""
    return pailiang,youhao


if __name__ == '__main__':


    crawlIndex()