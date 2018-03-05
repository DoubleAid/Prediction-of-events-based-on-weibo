import jieba
import pymongo
def buildStoplist():
    f = open(r'G:\学习笔记和实验\Python\stoplist.txt', 'r')
    stoplist = []
    for each in f:
        each = each.strip('\n').strip(' ').strip('\t')
        stoplist.append(each)
    stoplist.append('\n')
    stoplist.append(' ')
    stoplist.append('\t')
    stoplist.append('\u200b')
    return stoplist

def CalculateNum(target,words,calculate):
    '''
    此函数是为了统计每个词出现的次数
    stoplist:禁用词
    target：需要被统计的队列
    words：已经出现的子
    calculate：每个字出现的次数
    '''
    for word in target:
        if word not in words:
            calculate[word] = 1
            words.append(word)
        else:
            calculate[word]+=1
    return words,calculate
def buildList(data):#已去重！
    del (data['_id'])
    del (data['name'])
    list = []
    for each in data:
        list.append(data[each])
    list = [word for word in list if word not in stoplist]
    return list
def buildVector(words,list):#根据字和数列构建向量
    vec=[]
    for word in words:
        co=0
        for each in list:
            if each==word:
                co+=1
        vec.append(co)
    return vec
def connect():
    client=pymongo.MongoClient('mongodb://localhost:27017')
    database=client['结巴分词']
    co=database.collection_names()
    m=len(co)
    for i in range(0,m):
        print(str(i)+'-->'+co[i])
    name=input('请选择你要分词的表(输入N创建新的表):\n')
    db=co[int(name)]
    data=database[db]
    return data

def creatSaveCollection(name):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    database=client['分词向量']
    collection=database[name]
    return collection

def getData(dnum,data):
    n = data.count()
    if (dnum>n)|(dnum<=0):
        print('数组越界啦，没有这个数据')
    try:
        eachdata = data.find({'_id': str(dnum)})[0]
    except Exception as e:
        eachdata = data.find({'_id': dnum})[0]
    return eachdata


'''主函数'''
words=[]#words是该数据库里所有出现的有效词语
calculater={}#words里每一个词出现的次数
stoplist=buildStoplist()#stoplist是一个元祖
print('请选择分词数据库\n')
db=connect()
colname=db.name
savedb=creatSaveCollection(colname)
coun=db.count()#coun为数据库的数据个数
#######
print('正在生成词集合和统计各词的出现次数\n')
for term in range(1,coun+1):
    data=getData(term,db)
    list=buildList(data)
    words,calculater=CalculateNum(list,words,calculater)
print('所有词如下：\n',words)#生成所有词
print(calculater)#生成计数
for term in range(1,coun+1):
    print('正在处理第'+str(term)+'条数据')
    count=0
    src={}
    data=getData(term,db)#获取一条数据
    list=buildList(data)#构建已经去掉禁用词的元组
    vec=buildVector(words,list)
    src['_id']=term
    for each in vec:
        src[words[count]]=each
        count+=1
    savedb.save(src)
'''统计可用的词和出现的次数，以此给出权值'''
'''将字符提出，转化成向量'''

# print(string.replace('\n',''))
# segs=[word for word in t if word not in stoplist]
# print(segs)
# words=[]
# calculate={}
# for word in segs:
#     if word not in words:
#         calculate[word]=1
#         words.append(word)
#     else:
#         calculate[word]+=1
# print(calculate)