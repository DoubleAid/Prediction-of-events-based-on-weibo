'''关于聚类的方法的一些想法
1.聚类采用kmeans聚类方法
2.距离采用余弦距离
3.显示方法，求出所有数据的质心，
找离质心最远的与其最相似或最不相似的点的距离
作为高和宽
'''
import pymongo
import math
import random
import matplotlib.pyplot as plt

class kmean:
    maxangle=-1
    minangle=1
    k_value = 0
    database = ""
    dbname = ""
    dbsize = 0
    data = {}
    savebase=""
    def __init__(self):
        self.database = self.connect("value", 1)
        self.dbname = self.database.name
        self.dbsize = self.database.count()
        self.savebase=self.connect("result",2,self.dbname)
        value=input("请输入K的值")
        self.setKvalue(value)
        for each in range(1,int(value)+1):
            self.data[each-1]=""
        return

    def connect(self, Dname, myType, defaultname=None):  # 1表示读取数据的数据库，2表示存储数据的数据库
        client = pymongo.MongoClient('mongodb://localhost:27017')
        database = client[Dname]
        if myType == 1:
            co = database.collection_names()
            m = len(co)
            for i in range(0, m):
                print(str(i) + '-->' + co[i])
            name = input('请选择你所需的读取数据库:\n')
            db = co[int(name)]
            data = database[db]
            return data
        elif myType == 2:
            name = ""
            if defaultname == None:
                name = input("请输入存储数据库名称\n")
            else:
                name = defaultname
            data = database[name]
            return data

    def setKvalue(self, value):  #
        self.k_value = value

    def getData(self, dnum,database=""):
        base=self.database
        if database!="":
            base=database
        n = base.count()
        if (dnum > n) | (dnum <= 0):
            print('数组越界啦，没有这个数据')
        try:
            eachdata = base.find({'_id': str(dnum)})[0]
        except Exception as e:
            eachdata = base.find({'_id': dnum})[0]
        return eachdata

    def getKvalue(self):
        return self.k_value
    def getDistance(self,data1,data2):
        allcolumn = []
        distance=0
        newData1 = {}
        newData2 = {}

        for each in data1:
            allcolumn.append(each)
        for each in data2:
            if each not in allcolumn:
                allcolumn.append(each)
        for each in allcolumn:
            newData1[each] = 0
            newData2[each] = 0
        for each in allcolumn:
            if each in data1:
                newData1[each] = data1[each]
            if each in data2:
                newData2[each] = data2[each]
        for i in newData1:
            if i!="_id":
                distance+=pow(newData1[i]-newData2[i],2)
        return math.sqrt(distance)
    def getCOSDistance(self, data1, data2):
        if "Mclass" in data1:
            del(data1["Mclass"])
        if "Mclass" in data2:
            del(data2["Mclass"])
        numerator = 0
        denominator1 = 0
        denominator2 = 0
        allcolumn=[]
        newData1={}
        newData2={}

        for each in data1:
            allcolumn.append(each)
        for each in data2:
            if each not in allcolumn:
                allcolumn.append(each)
        for each in allcolumn:
            newData1[each]=0
            newData2[each]=0
        for each in allcolumn:
            if each in data1:
                newData1[each]=data1[each]
            if each in data2:
                newData2[each]=data2[each]
        for each in newData1:
            if each != "_id":
                numerator += newData1[each] * newData2[each]
        for each in newData1:
            if each != "_id":
                denominator1 += newData1[each] * newData1[each]
        for each in newData2:
            if each != "_id":
                denominator2 += newData1[each] * newData1[each]
        if (denominator2*denominator1)==0:
            return -1
        cos = numerator / (math.sqrt(denominator1 * denominator2))
        return cos

    def getEqua(self,data1,data2,num):
        allcolumn = []
        newData1 = {}
        newData2 = {}

        for each in data1:
            allcolumn.append(each)
        for each in data2:
            if each not in allcolumn:
                allcolumn.append(each)
        for each in allcolumn:
            newData1[each] = 0
            newData2[each] = 0
        for each in allcolumn:
            if each in data1:
                newData1[each]=data1[each]
            if each in data2:
                newData2[each]=data2[each]
        for each in newData1:
            self.data[num][each]=(newData1[each]+newData2[each])/2.0
        return
    def runs(self):
        print(self.k_value)
        for i in range(1, int(self.k_value)+1):
            num = random.randint(1, self.dbsize)
            self.data[i - 1] = self.getData(num)
            # for every in self.data[i-1]:
            #     print(every+":"+str(self.data[i-1][every]))
        for i in range(1,int(self.dbsize)+1):
            team=-1
            similar=-1000
            data=self.getData(i)
            for each in range(0,int(self.k_value)):
                num=self.getCOSDistance(data,self.data[each])
                if self.maxangle < num:
                    self.maxangle = num
                if self.minangle>num:
                    self.minangle=num
                if num>=similar:
                    team=each
                    similar=num
            print(team)
            self.getEqua(data,self.data[team],team)
            data["Mclass"]=team
            self.savebase.save(data)
        return

    def getCenterpoint(self):
        center=self.getData(1)
        del (center["_id"])
        for each in range(2,int(self.dbsize)):
            data=self.getData(each)
            for i in data:
                if i!="_id":
                    if i not in center:
                        center[i]=data[i]
                    else:
                        center[i]+=data[i]
            for i in center:
                center[i]/=2.0
        return center

    def display(self):
        center=self.getCenterpoint()
        mark=['or','ob','og','^r','+r','sr']
        max=-1
        min=1
        allv=0
        for i in range(1,int(self.dbsize)+1):
            data = self.getData(i, self.savebase)
            cos = self.getCOSDistance(center, data)
            allv+=cos
            if max<cos:
                max=cos
            if min>cos:
                min=cos
        print(max)
        allv=allv/float(self.dbsize)
        min=min-allv
        max=max-allv
        print(str(min)+" "+str(max)+" "+str(allv))
        for i in range(1,int(self.dbsize)+1):
            data=self.getData(i,self.savebase)
            color=data["Mclass"]
            cos=self.getCOSDistance(center,data)
            distance=self.getDistance(center,data)
            if cos>=allv:
                cos=cos/max
            else:
                cos=cos/min
            print(cos)
            x=distance*cos
            y=pow(distance,2)-pow(x,2)
            plt.plot(x,y,mark[int(color)],markersize=6)
        plt.show()
        return
if __name__ == '__main__':
    cluster=kmean()
    cluster.display()