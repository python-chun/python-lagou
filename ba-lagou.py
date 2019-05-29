import math

import requests
import os
import csv
import json
import time
import random
import pandas as pd
from matplotlib import path



class LagouSpider(object):

    def __init__(self):
        # user_agent 池
        self.USER_AGENT = [
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
        # 请求头
        self.headers = {
            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python开发?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
            'User-Agent': random.choice(self.USER_AGENT),
            'X-Requested-With': 'XMLHttpRequest'
        }
        #IP代理池
        # self.proxies = [
        # ]
        # 起始 url
        self.start_url = 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        # 目标 url
        self.target_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    # 保存 items
    def save_data(self, items):
        # 获取文件是否存在
         file_size = 'C:/Users/薛艳春/Desktop/python学习/拉钩爬虫可视化/analyst1.csv'
         if not os.path.exists(file_size):
            os.system(r"touch {}".format(path))
            # 表头
            name = ['公司名','公司ID','岗位','学历','工作年限要求','薪资','城市','公司人数',\
                    '是否融资', '职位诱惑','发布时间']
            # 建立DataFrame对象
            file_test = pd.DataFrame(columns=name, data=items)
            # 数据写入
            file_test.to_csv(r'analyst1.csv', encoding='utf-8', index=False)
            print("***************************************************/n")
         else:
             with open(r'analyst1.csv', 'a', newline='') as file_test:
                # 追加到文件后面
                writer = csv.writer(file_test,dialect='excel')
                # 写入文件
                writer.writerows(items)
                print("--------------------------------------------------------/n")

    # 请求起始 url 返回 cookies
    def get_start_url(self):
        session = requests.session()
        session.get(self.start_url, headers=self.headers,timeout=3)
        cookies = session.cookies
        return cookies

    # 将返回的 cookies 一起 post 给 target_url 并获取数据
    def post_target_url(self):
        cookies = self.get_start_url()
        pn = 1
        for pg in range(30):
            formdata = {
                'first': 'false',
                'pn': pn,
                'kd': 'python数据分析'
            }
            pn += 1
            print('第', pn, '页\n')
            response = requests.post(self.target_url, data=formdata, cookies=cookies,headers=self.headers, timeout=3, \
                                     )
            self.parse(response)
            time.sleep(20)      # 拉勾的反扒技术比较强，短睡眠时间会被封

    # 解析 response，获取 items
    def parse(self, response):
        print(response)
        items = []
        print(response.text)
        data = json.loads(response.text)['content']['positionResult']['result']

        if len(data):
            for i in range(len(data)):
                companyFullName = data[i]['companyFullName']   #公司全名
                companyShortName = data[i]['companyShortName'] #公司简称
                positionName = data[i]['positionName']         #岗位
                education = data[i]['education']               #学历
                workYear = data[i]['workYear']                 #工作年限要求
                salary = data[i]['salary']                     #薪资
                district = data[i]['district']                 #区域
                companySize = data[i]['companySize']           #公司规模
                financeStage = data[i]['financeStage']         #是否融资
                positionAdvantage = data[i]['positionAdvantage']#职位诱惑
                formatCreateTime = data[i]['formatCreateTime']  #发布时间
                list = [companyFullName,companyShortName,positionName,education,workYear,salary,district\
                        ,companySize,financeStage,positionAdvantage,formatCreateTime]
                items.append(list)
        self.save_data(items)
        time.sleep(1.3)


spider = LagouSpider()
spider.post_target_url()