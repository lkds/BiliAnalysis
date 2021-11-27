# from data import read_danmu
# from calculate import cal

# progress, danmu = read_danmu('pass')
# res = cal(danmu)
# print(res)

from locate import Analysis
from data import read_danmu
import requests

def send_cal_sentiment(word_list):
    url = 'http://127.0.0.1:8000/cal_sentiment'
    r = requests.post(url, json=word_list)
    return r.json()

def analysis():
    progress, word_list = read_danmu('data/海盗狗 copy.csv')
    res = send_cal_sentiment(word_list)
    a=Analysis(10,sentiment_list=[progress, res, word_list])
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
    # print('对应预览图',a.choose_pic('C:\\Users\\SuperPang\\Desktop\\何同学预览图'))

# analysis()