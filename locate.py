import matplotlib.pyplot as plt
from itertools import groupby
import csv
import os

class Analysis:
    """
    根据所给出的弹幕对应的情感值和弹幕的时间戳进行分片分析
    创建该类需要输入分片的时间长度（单位为秒）和保存数据的csv文件的路径
    情感值的取值范围定义在[-1，1]之间，而csv中的数据范围为[0,1]，读取文件后会在类内部会进行标准化
    会用到的数据包括：
    self.num_per_slit:一个长度为（视频长度/时间片长度）的列表，保存了每个时间片出现的弹幕总数
    self.pos_mean: 长度为（视频长度/时间片长度）的列表，为每个时间片中正向情感的均值
    self.neg_mean: 长度为（视频长度/时间片长度）的列表，为每个时间片中负向情感的均值
    self.data_differ: 每个时间片中正负向情感的差值
    """
    def __init__(self,slit, path = None, sentiment_list = None):
        """
        分析类初始化
        :param slit:  规定的分片时间段长度，单位为秒
        :param path: 文件路径
        """
        self.timestamp = []
        self.s_score = []
        self.x = [] # 弹幕
        self.slit=slit*1000  # 实际处理以毫秒为单位
        self.raw_slit=slit
        if path:
            self.load_csv(path)
        elif sentiment_list:
            self.timestamp = sentiment_list[0]
            self.s_score = sentiment_list[1]
            self.x = sentiment_list[2]
        else:
            raise ValueError('No data input')
        self.L = len(self.s_score)
        self.sort_data(self.timestamp,self.s_score,self.x)


    def normalize(self):
        """
        对情感极性分数进行归一化
        """
        for i in range(len(self.s_score)):
            self.s_score[i]=2*(self.s_score[i]-0.5)

    def load_csv(self, path):
        with open(path,'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            for item in reader:
                self.timestamp.append(int(item[0]))
                self.s_score.append(float(item[1]))
                self.x.append(item[2])
        # self.normalize()



    def sort_data(self,timestamp, s_score,x):
        self.timestamp= [x for x, y, z in sorted(zip(timestamp,s_score,x))]
        self.s_score = [y for x, y, z in sorted(zip(timestamp, s_score, x))]
        self.x = [z for x, y, z in sorted(zip(timestamp, s_score, x))]


    def count(self):
        """
        计算每一时间片内有多少弹幕数量
        :return: self.num_per_slit， 列表，长度为n，表示将弹幕按时间分为n段，每段时间片包含的弹幕数量
        """
        self.num_per_slit=[]
        max_time=self.timestamp[-1]
        self.n=int(max_time/self.slit)+1  # 一个视频分为n段
        for k, g in groupby(self.timestamp, key=lambda x: x//self.slit):
            self.num_per_slit.append(len(list(g)))
        return self.num_per_slit

    def mean(self):
        """
        计算每一个分片中，正向和负向情感的均值
        :return:self.pos_mean, self.neg_mean
        """
        i=0
        total=0
        self.total_mean=[]
        self.pos_mean=[]
        self.neg_mean=[]
        self.pos_sum=[]
        self.neg_sum=[]
        for k, g in groupby(self.timestamp, key=lambda x: x // self.slit):  # 对每一个分片
            length=len(list(g))
            pos_total=0
            neg_total=0
            pos_count=0
            neg_count=0
            for it in range(i, i+length):
                if self.s_score[it]>=0.5:
                    pos_total+=self.s_score[it]
                    pos_count=pos_count+1
                else:
                    neg_total+=self.s_score[it]
                    neg_count=neg_count+1

            self.pos_mean.append(pos_total/pos_count)
            self.neg_mean.append(neg_total/neg_count)
            self.pos_sum.append(pos_total)
            self.neg_sum.append(neg_total)
            self.total_mean.append((pos_total+neg_total)/(pos_count+neg_count))
            total=total+pos_total+neg_total
            i+=length
        self.whole_mean=total/self.L
        return self.pos_mean, self.neg_mean,self.pos_sum,self.neg_sum,self.total_mean

    def differ(self):
        """
        计算每个分段之间的正负情感均值的差值
        :return:
        """
        self.mean()
        self.data_differ=[]
        for i in range(len(self.pos_sum)):
            self.data_differ.append(self.pos_sum[i]-self.neg_sum[i])
        return self.data_differ

    def draw_pic(self):
        """
        画出三条曲线和一个柱状图，分别为
        正向情感均值变化
        负向情感均值变化
        差值变化
        弹幕数量统计
        :return:
        """
        plt.subplot(221)
        plt.plot(self.total_mean)
        plt.title("total_mean")

        plt.subplot(222)
        plt.plot(self.pos_mean)
        plt.title("pos_mean")

        plt.subplot(223)
        plt.plot(self.data_differ)
        plt.title("pos-neg mean")

        plt.subplot(224)
        plt.bar(x=range(0,len(self.data_differ)), height=self.data_differ)
        plt.title("num of barrage")

        plt.show()


    def choose_time(self):
        num = []
        for i,g in enumerate(self.num_per_slit):
            # 排除视频开始的第一个时间段
            if i==0:
                continue
            num.append([i+1,g])
        num = sorted(num,key = lambda x:x[1],reverse = True) # 降序，从大到小

        mean = []
        for i,g in enumerate(self.total_mean):
            if i==0:
                continue
            mean.append([i+1,g])
        mean = sorted(mean,key = lambda x:x[1],reverse = True)

        mean_differ = []
        for i,g in enumerate(self.differ()):
            if i==0:
                continue
            mean_differ.append([i+1,g])
        mean_differ = sorted(mean_differ,key = lambda x:x[1],reverse = True) 

        self.point = []

        # 选中发弹幕最多的时间段
        self.point.append(num[0][0])  
        # 是否选择弹幕第二多的时间段  要排除两个时间段距离过近的情况，同时第二多弹幕数/第一多弹幕数>60%
        if abs(num[0][0]-num[1][0]) > 4 and num[1][1] > num[0][1]*0.6 :
            self.point.append(num[1][0])  
        #
        choose_max_mean=True
        choose_second_mean=True
        for p in self.point:
            if abs(mean[0][0]-p) < 4:
                choose_max_mean=False
            if abs(mean[1][0]-p) < 4:
                choose_second_mean=False
        if choose_max_mean:
            self.point.append(mean[0][0])
        elif choose_second_mean:
            if abs(mean[0][0]-mean[1][0])>4:
                self.point.append(mean[1][0])
        #
        choose_max_differ=True
        choose_second_differ=True
        for p in self.point:
            if abs(mean_differ[0][0]-p) < 4:
                choose_max_differ=False
            if abs(mean_differ[1][0]-p) < 4:
                choose_second_differ=False
        if choose_max_differ:
            self.point.append(mean_differ[0][0])
        elif choose_second_differ:
            if abs(mean_differ[0][0]-mean_differ[1][0])>4:
                self.point.append(mean_differ[1][0])
      
        # self.point.append(mean[0][0]*10)
        # self.point.append(mean_differ[0][0]*10)
        self.point = [x*self.raw_slit for x in self.point]
        return self.point

    def choose_pic(self,dir_path): #预览图文件夹路径
        picture = []
        self.pic = []
        os.chdir(dir_path)
        for i in os.listdir():
            picture.append(int(os.path.splitext(i)[0]))
        picture = sorted(picture)
        for i in self.point:
            tmp = [abs(x-i) for x in picture]
            index = tmp.index(min(tmp))
            self.pic.append( str(picture[index-1])+'.jpg' )
        
        return self.pic

        
def test():
    # a=Analysis(20,u'data/[CURR]BV1CQ4y1U7kA_1.csv')
    a=Analysis(10,r'C:\Users\SuperPang\Desktop\何同学清洗.csv')

    a.count()
    num = a.num_per_slit
    print('弹幕总数:',num)
    print('弹幕最多时间段',(num.index(max(num))+1)*10)
    a.mean()
    print('情感均值:',a.total_mean)
#     print('负向情感均值:',a.neg_mean)
    a.differ()
    print('正负情感和值的差:',a.data_differ)
    print('选点',a.choose_time())
    print('对应预览图',a.choose_pic('C:\\Users\\SuperPang\\Desktop\\何同学预览图'))

#     a.draw_pic()


if __name__ == '__main__':
    test()