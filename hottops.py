# -*- encoding: utf-8 -*-
'''
@File    :   hottops.py
@Time    :   2020/05/04 08:50:19
@Author  :   JiahuaLink
@Version :   1.0
@Contact :   840132699@qq.com
@License :   (C)Copyright 2020
@Desc    :   获取新闻话题榜
'''

# here put the import lib

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

url="http://tieba.baidu.com/hottopic/browse/topicList?res_type=1"

def res_caputure():
    try:
        res = rq.get(url,timeout=30)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return "发生异常,响应码为{}".format(res.status_code)
    
if __name__ == "__main__":
    r = res_caputure()
    soup = BeautifulSoup(r)
    a = soup.select('a[target]')
    p = soup.select('span')
    soup_p=[]
    soup_a=[]
    s='10'
    
    if s=='':
        s=10
    else:
        s=int(s)
        
    for k in range(3,s*2+3,2):
        soup_p.append(p[k].string)
    for i in range(0,s):
        soup_a.append(a[i].string)
    dt={'排名':range(1,s+1),'标题':soup_a,'内容数':soup_p}
    df=pd.DataFrame(dt)
    print(df)
