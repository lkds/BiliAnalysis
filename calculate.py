# from api import client
import numpy as np
import paddlehub as hub

module = hub.Module(name='senta_bilstm')

def cal_sentiment(text_list):
    """
    计算情感倾向
    """
    res = module.sentiment_classify(text_list)
    sentiment_list = [(x['positive_probs'] - 0.5) * 2 for x in res]
    return sentiment_list

def cal_variance(sentiment_list):
    """
    计算情感倾向的方差
    """
    return np.var(sentiment_list)

def cal_ratio(sentiment_list):
    """
    计算负面情感占比
    """
    p_sum = np.sum([np.exp(x) - 1 if x >0 else 0 for x in sentiment_list])
    n_sum = np.sum([np.exp(-x) - 1 if x <0 else 0 for x in sentiment_list])
    return n_sum / (p_sum + n_sum)

def cal_mean(sentiment_list):
    """
    计算情感倾向的均值
    """ 
    pos_list = []
    neg_list = []
    for s in sentiment_list:
        if s > 0:
            pos_list.append(s)
        elif s < 0:
            neg_list.append(s)
    p_mean = np.mean(pos_list)
    n_mean = np.mean(neg_list)
    return p_mean, n_mean, np.mean(sentiment_list)

def cal(text_list):
    """
    计算情感倾向和方差
    """
    sentiment_list = cal_sentiment(text_list)
    variance = cal_variance(sentiment_list)
    ratio = cal_ratio(sentiment_list)
    mean = cal_mean(sentiment_list)
    return variance, ratio, mean
