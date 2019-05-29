# -*- coding: utf-8 -*-
import random

import requests
import math
import pandas as pd
import time
import threading
import sys


def get_json(url, page_num,position): # 接收两个参数：地址、页数
    USER_AGENT = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12'
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    ]

    '''从网页获取JSON,使用POST请求,加上头部信息'''
    headers = {
        'User-Agent':random.choice(USER_AGENT),
        'Host': 'www.lagou.com',
        'Referer':'https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    start_url = 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='

    session = requests.session()
    session.get(start_url, headers=headers,timeout=3)
    cookies = session.cookies

    data = {'first': 'true', 'pn': page_num, 'kd': position}
    response = requests.post(url, headers=headers,cookies=cookies,data=data)
    response.raise_for_status()  # 如果请求错误，则抛出错误代码
    response.encoding = 'utf-8'
    # 得到包含职位信息的字典
    page = response.json()
    return page


def get_page_num(count):
    '''计算要抓取的页数'''
    # 每页15个职位,向上取整
    res = math.ceil(count/15)
    # 拉勾网最多显示30页结果
    if res > 30:
        return 30
    else:
        return res


def get_page_info(jobs_list):
    '''对一个网页的职位信息进行解析,返回列表'''
    page_info_list = []
    for i in jobs_list:
        job_info = []
        job_info.append(i['positionName'])          # 职位名称
        job_info.append(i['companyFullName'])       # 公司全名
        job_info.append(i['companyShortName'])      # 公司简称
        job_info.append(i['companySize'])           # 公司规模
        job_info.append(i['city'])                  # 城市
        job_info.append(i['district'])              # 区域
        job_info.append(i['workYear'])              # 工作经验
        job_info.append(i['education'])             # 学历要求
        job_info.append(i['salary'])                # 工资
        job_info.append(i['financeStage'])          # 融资阶段
        job_info.append(i['positionAdvantage'])     # 职位福利
        page_info_list.append(job_info)
    return page_info_list


def main():
    # 第一步：确定获取数据的URL
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
    # 第二步：请求数据，获取总的职位数
    position = input("输入需要查询的职位：")
    page_one = get_json(url,1,position) # 先设定页数为1,获取总的职位数
    total_count = page_one['content']['positionResult']['totalCount']
    # 2.1 根据总的职位数，根据每页15个职位数分割，最后得到请求的次数
    num = get_page_num(total_count)
    # 2.2 第一次请求后暂停20秒，防止被封；
    time.sleep(20)
    print('职位总数:{},页数:{}'.format(total_count, num))

    total_info = []  # 存储所有抓取的数据
    for n in range(1, num+1):
        # 对每个网页读取JSON, 获取每页数据
        page = get_json(url,n,position)
        jobs_list = page['content']['positionResult']['result']
        page_info = get_page_info(jobs_list)
        total_info += page_info
        print('已经抓取第{}页, 职位总数:{}'.format(n, len(total_info)))
        # 每次抓取完成后,暂停一会,防止被服务器拉黑
        time.sleep(20)
    # 将总数据转化为data frame再输出
    df = pd.DataFrame(data=total_info, columns=['职位名称','公司全名','公司简称','公司规模','城市','区域','工作经验','学历要求','工资','融资阶段','职位福利'])
    df.to_csv('C:/Users/薛艳春/Desktop/python学习/拉钩爬虫可视化/python3.csv',index=False)
    print('已保存为csv文件.')

if __name__ == "__main__":
    main()