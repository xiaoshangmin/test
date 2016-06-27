# -*- coding:utf-8 -*-
__author='xiaoshangmin'
import requests
import json
import os
from concurrent import futures
import time
from tqdm import *
url = 'https://www.instagram.com/{}/media?&max_id={}'
def ins(username,items=[],max_id=''):
    getimgurl = url.format(username,max_id)
    #print(getimgurl)
    r = requests.get(getimgurl)
    item =json.loads(r.text)
    for i in item['items']:
        imgurl = i['images']['standard_resolution']['url']
        items.append(imgurl)
    if item['more_available'] is True and item['status']=='ok':
        max_id=item['items'][-1]['id']
        return ins(username,items,max_id)
    else:
        #downloads(items)
        return items
def downloads(items,save_dir='./img'):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    print('开始下载')
    r = requests.get(items)
    imgname = items.split('/')[-1].split('?')[0]
    save = os.path.join(save_dir,imgname)
    with open(save,'wb') as f:
        f.write(r.content)
if __name__=='__main__':
    with futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_item = {}
        for item in ins('put username'):
            future = executor.submit(downloads,item)
            future_item[future] = item

        for f in tqdm(futures.as_completed(future_item),total=len(future_item),desc='Downloading'):
            item = future_item[f]
            if f.exception() is not None:
                print('%r generated an exception: %s') % (item, f.exception())