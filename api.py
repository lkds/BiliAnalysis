# from aip import AipNlp

# """ 你的 APPID AK SK """
# client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
# print(client.sentimentClassify(['''我可以很负责的说，番茄能走到这一步绝对不是单凭搞笑视频和合作综艺。''','''他有着他的思想，他的才华，他将这一切都灌输到自己的作品里，虽然流量远不如其他，但他一直在做，并且越做越好越做越勤，从烂俗笑话，到杀手，小学生，破这个案子，再到现在，他一直保持着初心，从未变过''']))

# import paddlehub as hub
# module = hub.Module(name='senta_bilstm')
# res = module.sentiment_classify(['我可以很负责的说，番茄能走到这一步绝对不是单凭搞笑视频和合作综艺。'])
# print(res)


from fastapi import FastAPI
import uvicorn

from starlette.middleware.cors import CORSMiddleware  #引入 CORS中间件模块

#创建一个FastApi实例
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

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/video_analysis/{bvid}")
def video_analysis(bvid: str):
    return {"bv":bvid}

@app.get("/video_list/up/{upid}")
def up_analysis(upid: str):
    pass

@app.get('/video_list/hot')
def hot_analysis():
    pass

uvicorn.run(app, host="0.0.0.0", port=5000)