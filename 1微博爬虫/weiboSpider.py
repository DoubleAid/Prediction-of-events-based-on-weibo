'''
这是一个微博话题爬虫
'''
import time
import requests
import re
from lxml import etree
from pymongo import MongoClient

class spider():
    cook=[]
    header={}
    url={}
    title=''
    databaseSet={'db_name':'','table_name':'','link':''}
    collection=''

    def convertAnddisplay(self,text,color=''):
        string = text
        try:
            string = str(string, "utf-8")
        except Exception as e:
            print('\033[1;31m转换时出错，请检查字符串的编码\033[0m')
            exit(0)
        self.display(string,color)

    def display(self,text,color=''):
        if color=='':
            print(text)
        elif color=='red':
            '''红色作为错误输出'''
            print('\033[1;31m',end='')
            print(text,end='')
            print('\033[0m')
        elif color=='blue':
            '''蓝色作为提示输出'''
            print('\033[1;36m',end='')
            print(text,end='')
            print('\033[0m')
        elif color=='green':
            '''绿色作为信息输出'''
            print('\033[1;32m',end='')
            print(text,end='')
            print('\033[0m')

    def getCook(self):
        while True:
            cookie = {}
            text = input('请输入你的cookies:\n')
            cookie['Cookie'] = text
            self.cook.append(cookie)
            co=0
            while (co!='1')&(co!='2'):
                co = input('是否继续输入？：\n1-->继续\n2-->退出\n')
            if co == '1':
                continue
            else:
                break

    def sleep(self,setTime):
        time.sleep(setTime)

    def __init__(self):
        while(True):
            i=int(input('\033[1;36m请输入你的选择:\n'+'1-->使用默认的cookies\n2-->添加cookies\n\033[0m'))
            if i==1:
                cook = {
                    'Cookie': '_T_WM=2d2154427a21f9573c1495c91a8053a4; gsid_CTandWM=4u20f8f21tr8Ded1; ALF=1519364911; SCF=AvID83VzAmxEH1Yl-17zo7BoeImaNGJ_aE54FJFp01neZqwuzqkHpCimIWmCnNdUOpbBUupTZ_dltY104zlKdGM.; SUB=_2A253bAAMDeRhGeBM7lEU8SbNzD2IHXVUrqBErDV6PUJbktBeLXjikW1NRMmhJjSOfBu3dzG1u_R0aW0iJ5NoHZZl; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5HJGnRiQ.gbA6Q9CjgPFqg5JpX5K-hUgL.FoqESKefeKnpS022dJLoIEBLxKqL1hnL1K2LxK-L1K-L122LxKBLBonLB-2LxK-L1K2LBont; SUHB=0U1JSbGgsDUiUi; SSOLoginState=1516793948'
                }
                self.cook.append(cook)
                break
            elif i==2:
                self.getCook()
                break
            else:
                continue
        self.title=input('\033[1;36m请输入你要查找的内容:\n\033[0m')
        self.url['start_url']='https://weibo.cn/search/?tf=5_012'
        self.url['post_url']='https://weibo.cn/search/?pos=search'
        self.url['connect_url']='https://weibo.cn'
        i=input('是否使用默认的数据库设置?\ny/Y-->是\nn/N-->否')
        if (i=='N')| (i=='n'):
            self.databaseSet['db_name']=input('请输入数据库名称：\n')
            self.databaseSet['table_name'] = input('请输入操作的表的名称：\n')
            self.databaseSet['link']=input('请输入服务器地址：\n')
        else:
            self.databaseSet['db_name']='微博数据'
            self.databaseSet['table_name'] = self.title
            self.databaseSet['link'] = 'mongodb://localhost:27017'
        client = MongoClient(self.databaseSet['link'])
        db = client[self.databaseSet['db_name']]
        self.collection = db[self.databaseSet['table_name']]
    def getInfo(self,selector):
        blogs=selector.xpath('//*[@class="c" and starts-with(@id,"M_F")]')
        for eachblog in blogs:
            name=eachblog.xpath('div/a[@class="nk"]/text()')[0]
            print(name)
            span=eachblog.xpath('div/span[@class="ctt"]')[0]
            content=span.xpath('string(.)')
            if content:
                print(content)
            else:
                print('无')
            data={}
            data['name']=name
            data['content']=content
            self.savedata(data)

    def prase(self):
        flag=False
        self.display('正在初始化中...','blue')
        for each in self.cook:
            self.display(each,'red')
        print('cookies初始化完成！')
        html=requests.get(self.url['start_url'],headers=self.header,cookies=self.cook[0]).content
        '''初始化检测是否能到搜索界面
            如果能到，标题是搜索结果
        '''

        data={'smblog':'搜微博'}
        data['keyword']=self.title
        post_info= requests.post(self.url['post_url'], cookies=self.cook[0], headers=self.header, data=data)
        self.sleep(2)
        post_html=post_info.content
        content='start'
        while content:
            selector=etree.HTML(post_html)
            content=selector.xpath('//div[@class="pa"]/form/div/a[1]/@href')
            self.getInfo(selector)
            if content:
                content=content[0]
            else:
                print('结束')
                break
            new_url=self.url['connect_url']+content
            pageNum=re.findall('page=(\d+)',new_url)[0]
            print('正在爬取第'+pageNum+'页...')
            if flag==True:
                self.display('爬虫爬取'+self.title+'完成！')
                exit(0)
            elif (int(pageNum)==100)&(flag==False):
                flag=True
            post_html = requests.get(new_url, headers=self.header, cookies=self.cook[0]).content
            self.sleep(4)

    def savedata(self,data):

        count=int(self.collection.count())
        count=str(count+1)
        data['_id']=count
        print('正在保存'+count+'数据')
        self.collection.save(data)

a = spider()
a.prase()