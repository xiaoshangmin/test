import pymysql,time
from functools import reduce

start = time.clock()
def add(x, y):
    if y=='市辖区':
        return x
    return x + y

db = pymysql.connect('localhost', 'root', '', 'test')
db.set_charset('utf8')
cursor = db.cursor()
file = open('region.txt', 'r', encoding='utf-8')
while 1:
    lines = file.readlines(8192)
    if not lines:
        break
    for line in lines:
        l = line.strip().split(',')
        ll = []
        for i in range(0, len(l)):
            if l[i] == '""':
                continue
            ll.append(l[i].strip('"'))
        length = len(ll)
        if length == 2:
            sql = "INSERT INTO citymore(loc_id,loc_name) values('%s','%s')" % (
                ll[0], ll[length - 1])
        else:
            sql = "INSERT INTO citymore(loc_id,loc_name,paddr) values('%s','%s','%s')" % (
            ll[0], ll[length - 1], reduce(add, ll[1:length - 1]))
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
file.close()
db.close()
end = time.clock()
print('run time is %.03f seconds' % (end-start))#About half an hour
