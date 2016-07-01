# -*-coding:utf-8-*-
__author__ = 'xiaoshangmin'
from bs4 import BeautifulSoup
import requests, pymysql, re, json

DEBUG = False
GSQL = True
GJSON = False


def conn(localhost, user, password, database):
    db = pymysql.connect(localhost, user, password, database)
    db.set_charset('utf8')
    return db


def getprovince(style):
    # pinfo = province.find('tr').get_text(',', strip=True)
    return re.compile("#FFDF80").search(str(style))


# 获取城市
def getcity(style):
    return re.compile("#CCFFFF").search(str(style)) or re.compile("#E6E6FA").search(str(style))


# 只有二级区域
def onlyregion(style):
    return re.compile("#EFEFEF").search(str(style))


def saveDataAsJson(val):
    with open('city.json', 'a') as f:
        if f:
            json.dumps(',', f)
        json.dump(val, f)


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
    for province in rs:
        pinfo = province.find(style=getprovince)  # 获取省级
        pinfo = pinfo.get_text(',', strip=True)
        plist = pinfo.split(',')
        upaddr = plist[1]
        if GSQL:
            # saveData(db, *plist)
            pass
        else:
            # saveDataAsJson(*plist)
            pdict = [{'code': plist[0], 'name': plist[1]}]

        city = province.find_all(style=getcity)  # 获取城市
        if city:
            # pdict[0]['child'] = []
            for c in city:
                cinfo = c.get_text(',', strip=True).split(',')
                cinfo.append(upaddr)
                if GSQL:
                    # saveData(db, *cinfo)
                    pass
                else:
                    # saveDataAsJson(*cinfo)
                    pdict[0]['child'].append({'code': cinfo[0], 'name': cinfo[1]})
                code = cinfo[0][:4]
                county = c.find_next_siblings()
                for y in county:
                    yinfo = y.find_all(string=re.compile(code));  # 获取区域
                    if yinfo:  # 县级
                        for yy in yinfo:
                            yinfos = [yy, yy.find_next().get_text(), upaddr + cinfo[1]]
                            if GSQL:
                                # saveData(db, *yinfos)
                                pass
                            else:
                                # saveDataAsJson(*yinfos)
                                # pdict['child']['child'].append({'code': yinfos[0], 'name': yinfos[1]})
                                pass
                                # saveDataAsJson(pdict)

        else:
            # city = province.find_all(style=onlyregion)  # 获取二级区域
            city = province.find_all(string=re.compile(str(31)))
            for c in city:
                # cinfo = c.get_text(',', strip=True).split(',')
                cinfo = c.find_next().get_text()
                if cinfo == '县':
                    continue
                clist = range(0, len(cinfo), 2)
                for c in clist:
                    ppp = cinfo[c:c + 2]
                    # print(ppp)
                    if ppp[0].isdigit():  # 香港无行政区代码不保存
                        ppp.append(upaddr)
                        if GSQL:
                            # saveData(db, *ppp)
                            pass
                        else:
                            # saveDataAsJson(*ppp)
                            # plist.append(ppp)
                            pass


if __name__ == "__main__":
    # DEBUG = True
    # GSQL = False
    db = conn('localhost', 'root', '', 'test')
    # 维基百科地址
    urls = [
        # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(1%E5%8C%BA)',
        # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(2%E5%8C%BA)',
        'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(3%E5%8C%BA)',
        # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(4%E5%8C%BA)',
        # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(5%E5%8C%BA)',
        # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(6%E5%8C%BA)',
        # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(7%E5%8C%BA)',
        # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81_(8%E5%8C%BA)'
    ]
    for url in urls:
        r = requests.get(url)
        r.encoding = 'utf-8'
        bs = BeautifulSoup(r.content, 'html.parser')
        rs = bs.find_all('table', class_="wikitable")
        save_area(rs, db)
    db.close()
