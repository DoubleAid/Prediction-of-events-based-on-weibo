'''
本程序为生成特定词的IDF和指定文章词的TF
'''
# 有很多不同的数学公式可以用来计算TF-IDF。
# 这边的例子以上述的数学公式来计算。
# 词频 (TF) 是一词语出现的次数除以该文件的总词语数。
# 假如一篇文件的总词语数是100个，而词语“母牛”出现了3次，
# 那么“母牛”一词在该文件中的词频就是3/100=0.03。一
# 个计算文件频率 (IDF) 的方法是文件集里包含的文件总数除以测定有多少份文件出现过“母牛”一词。
# 所以，如果“母牛”一词在1,000份文件出现过，而文件总数是10,000,000份的话，
# 其逆向文件频率就是 lg10,000,000 / 1,000)=4。
# 最后的TF-IDF的分数为0.03 * 4=0.12.
'''为了实现TF-IDF的实现
分两步走：
1.实现TF
2.实现IDF'''
import pymongo
import math
def connect(Dname,myType,defaultname=None):#1表示读取数据的数据库，2表示存储数据的数据库
    client=pymongo.MongoClient('mongodb://localhost:27017')
    database=client[Dname]
    if myType==1:
        co=database.collection_names()
        m=len(co)
        for i in range(0,m):
            print(str(i)+'-->'+co[i])
        name=input('请选择你所需的读取数据库:\n')
        db=co[int(name)]
        data=database[db]
        return data
    elif myType==2:
        name=""
        if defaultname==None:
            name=input("请输入存储数据库名称\n")
        else:
            name=defaultname
        data=database[name]
        return data

def build(list,database,savebase):
    '''构建权值向量'''
    total=database.count()
    for each in range(1,total+1):
        data=getData(each,database)
        for every in data:
            if (data[every]!=0)&(every!="_id"):
                data[every]=data[every]*list[every]
        savebase.save(data)

    return
def getData(dnum,data):
    n = data.count()
    if (dnum>n)|(dnum<=0):
        print('数组越界啦，没有这个数据')
    try:
        eachdata = data.find({'_id': str(dnum)})[0]
    except Exception as e:
        eachdata = data.find({'_id': dnum})[0]
    return eachdata
def disposeTF(num,database,savebase):
    data = getData(num, database)
    wordcount = 0
    word = {}
    for every in data:
        if (data[every] != 0) & (every != "_id"):
            print(str(every) + ':' + str(data[every]))
            word[every] = data[every]
            wordcount += data[every]
    print(wordcount)
    for each in word:
        word[each] = (float)(word[each]) / wordcount
        print(each + ":" + str(word[each]))
    word["_id"]=num
    savebase.save(word)
def disposeIDF(database):
    list={}
    data=getData(1,database)
    del (data['_id'])
    for each in data:
        list[each]=0
    total=database.count()
    for each in range(1,total+1):
        data = getData(each, database)
        for every in data:
            if (data[every]!=0)&(every!="_id"):
                list[every]+=1
    for each in list:
        list[each]=math.log10(total)/(float)(list[each])
    return list

if __name__ == '__main__':
    data={}
    IDFWord={}
    database=connect("分词向量",1)
    print(database.name)
    savebase=connect("TF结果",2,database.name)
    Finalbase=connect("value",2,database.name)
    for each in range(1,database.count()+1):
         disposeTF(each,database,savebase)
    IDFList=disposeIDF(database)
    for each in IDFList:
        print(each+":"+str(IDFList[each]))
    build(IDFList,savebase,Finalbase)