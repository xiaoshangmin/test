# -*-coding:utf-8-*-
__author__ = 'xiaoshangmin'
from bs4 import BeautifulSoup
import requests
import pymysql
import re

DEBUG = False


def conn(localhost, user, password, database):
    db = pymysql.connect(localhost, user, password, database)
    return db


# 获取城市
def getcity(style):
    return re.compile("#CCFFFF").search(str(style)) or re.compile("#E6E6FA").search(str(style))


# 只有二级区域
def onlyregion(style):
    return re.compile("#EFEFEF").search(str(style))


def savedata(db, *val):
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


def save_area(rs, db):
    for province in rs:
        pinfo = province.find('tr').get_text(',', strip=True)  # 获取省级
        plist = pinfo.split(',')
        upaddr = plist[1]
        savedata(db, *plist)

        city = province.find_all(style=getcity)  # 获取城市
        if city:
            for c in city:
                cinfo = c.get_text(',', strip=True).split(',')
                # cinfo = cinfo.split(',')
                cinfo.append(upaddr)
                savedata(db, *cinfo)
                code = cinfo[0][:4]
                county = c.find_next_siblings()
                for y in county:
                    yinfo = y.find_all(string=re.compile(code));
                    if yinfo:  # 县级
                        for yy in yinfo:
                            yinfos = [yy, yy.find_next().get_text(), upaddr + cinfo[1]]
                            savedata(db, *yinfos)

        else:
            city = province.find_all(style=onlyregion)  # 获取二级区域
            for c in city:
                cinfo = c.get_text(',', strip=True).split(',')
                clist = range(0, len(cinfo), 2)
                for c in clist:
                    ppp = cinfo[c:c + 2]
                    if ppp[0].isdigit():  # 香港无行政区代码不保存
                        ppp.append(upaddr)
                        savedata(db, *ppp)


if __name__ == "__main__":
    # DEBUG = True
    db = conn('localhost', 'root', '', 'test')
    db.set_charset('utf8')

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
    for url in urls:
        r = requests.get(url)
        r.encoding = 'utf-8'
        bs = BeautifulSoup(r.content, 'html.parser')
        rs = bs.find_all('table', class_="wikitable")
        save_area(rs, db)
    db.close()
