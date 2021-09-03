from fastapi import FastAPI, Form
from pydantic import BaseModel
app = FastAPI()
from xxx import Class

ocr = Class()

# def pack_json():
#     re = {"code":2000}
    


class pdfItem(BaseModel):
    pdf_file : str

@app.get("/run")
def get_1():
    return {"status":"ok"}

@app.post("/api/pdfocr")
def pdfocr(args:pdfItem):
    print(len(args.pdf_file))
    # 接受文件
    # 。。。
    # PDF 预处理
    # 对于 PDF 每个页码转图片
    # 对于每一个图片 转 ndarray
    # result = ocr.ocr(ndarray)
    # 打包 json
    # return json
    return {"status":"ok"}

@app.post("api/voice2word/")
def voice2word(**args):
    # 接受文件
    # 限制 wav
    # result = voicecor()
    # 打包 json
    # return json

@app.post("api/videoocr/")
def videoocr(**args):
    # 接收文件
    # 获得视频基本参数

    # 切五帧 跑五帧 对于每个识别框
    
    # 获得 result 
    # {frame: , data:"123123"}

    # 处理第一次出现
    # set( )

    # 转时间
    # 打包

@app.post("api/videocheck/")
def videocheck(**args):
    # 读取文件
    # 获得第一帧
    # 根据 id 画框
    # 返回图片 + json
    # form-data

