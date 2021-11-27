import os
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware  #引入 CORS中间件模块
import uvicorn

# 加载
device = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = BertTokenizer.from_pretrained('hfl/chinese-bert-wwm')   # 分词器
bert = BertModel.from_pretrained('hfl/chinese-bert-wwm').to(device)
# 网络结构
class Net(nn.Module):
    def __init__(self, input_size):
        super(Net, self).__init__()
        self.fc = nn.Linear(input_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc(x)
        out = self.sigmoid(out)
        return out

net = torch.load("weights/bert_dnn_8.model").to(device)

def process_batch(batch):
    global net
    tokens = tokenizer(batch, padding=True)
    input_ids = torch.tensor(tokens["input_ids"]).to(device)
    attention_mask = torch.tensor(tokens["attention_mask"]).to(device)
    with torch.no_grad():
        last_hidden_states = bert(input_ids, attention_mask=attention_mask)
        bert_output = last_hidden_states[0][:, 0]
    outputs = net(bert_output)
    outputs = outputs.T[0].tolist()
    return outputs


def process_list(s, seg=20):
    global net
    res = []
    last = 0
    for i, d in enumerate(s):
        if i!= 0 and i % seg == 0:
            res += process_batch(s[i-seg:i])
            last = i
    rest = s[last:]
    if rest:
        res += process_batch(rest)
    # arr = np.array(res)
    return res

# print(process_batch(['哈哈哈哈哈','这是什么啊','我叫阿杰,他们都叫我杰哥','前方高能']))
app = FastAPI()
#设置允许访问的域名
origins = ["*"]  #也可以设置为"*"，即为所有。

#设置跨域传参
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  #设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  #允许跨域的headers，可以用来鉴别来源等作用。

@app.post('/cal_sentiment')
def cal(data:list):
    res = process_list(data)
    return res

uvicorn.run(app, host="0.0.0.0", port=8000)