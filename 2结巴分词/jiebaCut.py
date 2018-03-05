import jieba
import pymongo
'''自定义词组'''
def buildSDefine():
    f = open(r'G:\学习笔记和实验\Python\freestyle.txt', 'r')
    freeStyle = []
    for each in f:
        each = each.strip('\n').strip(' ').strip('\t')
        freeStyle.append(each)
    return freeStyle
selfdefine=buildSDefine()
for each in selfdefine:
    print(each)
    jieba.suggest_freq(each,True)
''''''
client=pymongo.MongoClient('mongodb://localhost:27017')
n=client.database_names()
m=len(n)
for i in range(0,m):
    print(str(i)+'-->'+n[i])
db=n[int(input('请选择你要分词的数据库:\n'))]
print(db)
database=client[db]
resultdb=client['结巴分词']
''''''
co=database.collection_names()
m=len(co)
for i in range(0,m):
    print(str(i)+'-->'+co[i])
db=co[int(input('请选择你要分词的表:\n'))]
result=resultdb[db]
print(db)
data=database[db]
n=data.count()
print(n)
for num in range(1,n+1):
    Mdata={}
    eachdata=data.find({'_id':str(num)})[0]
    content=eachdata['content']
    list=jieba.tokenize(content)
    #print(str(num)+string)
    Mdata['_id']=eachdata['_id']
    Mdata['name']=eachdata['name']
    count=0
    for each in list:
        word='Term'+str(count)
        Mdata[word] = each[0]
        count+=1
    result.save(Mdata)