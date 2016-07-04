# -*-coding:utf-8-*-
__author__ = 'xiaoshangmin'
from bs4 import BeautifulSoup
import requests, pymysql, re, json, time

DEBUG = False
GSQL = True
GJSON = False

# 连接数据库
def conn(localhost, user, password, database):
    db = pymysql.connect(localhost, user, password, database)
    db.set_charset('utf8')
    return db


# 获取省级
def getprovince(style):
    # pinfo = province.find('tr').get_text(',', strip=True)
    return re.compile("#FFDF80").search(str(style))


# 获取城市
def getcity(style):
    return re.compile("#CCFFFF").search(str(style)) or re.compile("#E6E6FA").search(str(style))


def saveDataAsJson(val):
    with open('city.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(val,ensure_ascii=False))


def saveData(db, *val):
    if len(val) == 2:
        sql = "INSERT INTO city(loc_id,loc_name) values(%s,'%s')" % (val[0], val[1])
    elif len(val) == 3:
        sql = "INSERT INTO city(loc_id,loc_name,paddr) values(%s,'%s','%s')" % (val[0], val[1], val[2])
    else:
        print('parameter error')
        exit()
    cursor = db.cursor()
    if DEBUG:
        print(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


# def saveway(lists, db=None):
#     if (db):
#         saveData(db, *lists)
#     else:
#         saveDataAsJson(*lists)


def save_area(rs, db=None):
    i = 0
    citydata = []
    for province in rs:
        pinfo = province.find(style=getprovince)
        pinfo = pinfo.get_text(',', strip=True)
        plist = pinfo.split(',')
        upaddr = plist[1]
        if GSQL:
            saveData(db, *plist)
        else:
            citydata.append({'code': plist[0], 'name': plist[1], 'child': []})
        city = province.find_all(style=getcity)
        if city:
            j=0
            for c in city:
                cinfo = c.get_text(',', strip=True).split(',')
                cinfo.append(upaddr)
                if GSQL:
                    saveData(db, *cinfo)
                else:
                    citydata[i]['child'].append({'code': cinfo[0], 'name': cinfo[1],'upaddr':upaddr,'child':[]})
                code = cinfo[0][:4]
                county = province.find_all(string=re.compile(code))
                county.pop(0)
                cpaddr = cinfo[2] + cinfo[1]
                for y in county:
                    yinfo = y.find_next().get_text()
                    if yinfo:
                        yinfos = [y, yinfo, cpaddr]
                        if GSQL:
                            saveData(db, *yinfos)
                        else:
                            citydata[i]['child'][j] ['child'].append({'code': y, 'name': yinfo,'upaddr':cpaddr})
                j=j+1

        else:
            city = province.find_all(string=re.compile(str(plist[0][0:2])))
            city.pop(0)
            for c in city:
                cinfo = c.find_next().get_text()
                if cinfo == '县' or cinfo.isdigit():
                    continue
                data = [c, cinfo, upaddr]
                if GSQL:
                    saveData(db, *data)
                else:
                    citydata[i]['child'].append({'code':c,'name':cinfo,'upaddr':upaddr})

        i=i+1
    return citydata



if __name__ == "__main__":
    GSQL = False
    start = time.clock()
    #db = conn('localhost', 'root', '', 'test')
    # 维基百科地址
    urls = [
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(1%E5%8C%BA)',
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(2%E5%8C%BA)',
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(3%E5%8C%BA)',
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(4%E5%8C%BA)',
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(5%E5%8C%BA)',
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(6%E5%8C%BA)',
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(7%E5%8C%BA)',
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(8%E5%8C%BA)'
    ]
    c = []
    for url in urls:
        r = requests.get(url)
        r.encoding = 'utf-8'
        bs = BeautifulSoup(r.content, 'html.parser')
        rs = bs.find_all('table', class_="wikitable")
        if GSQL:
            save_area(rs, db)
        else:
            data = save_area(rs)
            for n in range(0,len(data)):
                c.append(data[n])
    saveDataAsJson(c)
    #db.close()
    end = time.clock()
    print('run time is %.03f seconds' % (end - start))
