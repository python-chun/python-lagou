#!/usr/bin/env python
#_*_coding:utf-8_*_
__author__ = 'Tiger'
import re
import requests
import json
import threading


def get_songid_by_name(name,start):
    print(start)
    '''通过歌手获取歌曲信息song_id'''
    url='http://music.baidu.com/search/song?s=1&size=20&third_type=0'
    data={
        'key':name,
        'start':start,
        'size':20,
        'third_type':0,
        's' : 1,
        'jump' : 0
    }
    response=requests.get(url,params=data)
    html=response.text
    # reg="pageNavigator:{ 'total':(.*?), 'size':(.*?), 'start':0, 'show_total':0, 'focus_neighbor':0 }"
    # for total,size in re.findall(reg,html,re.S):
    #     print(total,size)
    #     num=int(total)//int(size)
    #     print(num)
    #需要用到正则表达式来匹配
    reg='&quot;sid&quot;:(.*?),'
    song_ids=re.findall(reg,html,re.S)
    #返回为列表
    return song_ids



def get_mp3_by_sid(sid):
    '''通过song_id 下载mp3'''
    api='http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&songid=%s'%sid
    response=requests.get(api)
    html=response.text #获取返回信息
    data=json.loads(html)#讲字符串转化为json格式
    title=data['songinfo']['title']
    mp3_url=data['bitrate']['file_link']
    title = re.sub(',|"|\?', '', str(title))
    with open(r'E:\pyCharm setup\Desktop\Taylor Swift\%s.mp3 '%str(title),'wb') as f:
        f.write(requests.get(mp3_url).content)
        print('%s 下载完成'%title)
def get_pagenumb(name):
    '''
    获取总页数
    :param name:
    :return: 返回页数
    '''
    url = 'http://music.qianqian.com/search'
    data = {
        'key': name
    }
    response = requests.get(url, params=data)
    html = response.text
    num=0
    reg="pageNavigator:{ 'total':(.*?), 'size':(.*?), 'start':0, 'show_total':0, 'focus_neighbor':0 }"
    for total,size in re.findall(reg,html,re.S):
        num=int(total)//int(size)
        if num >int(total)/int(size):
            num=num-1
    return num,int(size)

def start_donwload(name,size):
    for sid in get_songid_by_name(name,size):
        get_mp3_by_sid(sid)
def main(name):
    num,size=get_pagenumb(name)
    print(type(size))
    print('一共%s页，每%d页歌曲'%(num,size))
    for i in range(num+1):
        start_size=i*size
        print(i,size)
        print('start_size:%s'%start_size)
        t=threading.Thread(target=start_donwload,args=(name,start_size))
        t.start()

if __name__ == '__main__':
    name=input('输入歌曲，歌手或者专辑名:')
    main(name)