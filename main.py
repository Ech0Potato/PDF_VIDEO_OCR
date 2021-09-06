from numpy import matrix
from typing import Dict, ItemsView
from fastapi import FastAPI, Form , File , UploadFile , Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import fitz
import numpy as np
import cv2
from chineseOCR import Chinese_OCR
from return_data_struct import get_pdf_ocr_return_json
from return_data_struct import get_voice_2_word_return_json
from voiceOCR import voiceOCR
import os
import json
from starlette.responses import StreamingResponse, FileResponse
import io
import math
from starlette.routing import Host
import copy
import filetype
app = FastAPI()
ocr = Chinese_OCR()

templates = Jinja2Templates(directory="/root/static")

def pack_error_json(message):
    
    re = {
        "code" : 4000,
        "message" : message,
        "data" : ""
    }

    return re

# 返回数据
def pack_json(code ,data):
    if code == 2000:
        re = {
            "code":2000,
            "message":"视频OCR执行成功",
            "data": data
        }
    if code == 4000:
        re = {
            "code":4000,
            "message":"视频OCR执行失败",
            "data": data
        }
    if code == 6000:
        re = {
            "code":4000,
            "message":"视频文件格式错误或已损坏",
            "data": data
        }
    return re  

'''
words:[
    {"location":[[x1,y1],[x2,y2]], "content":"xxxxxxx"}
    ......
]
'''
def get_words(re_list):
    words = []
    for re in re_list:
        words.append({"location":re[0],"content":re[1]})
    return words

# 把秒转换成 分：秒：毫秒（xx:xx.xxx）
def transfer_time(temp_time):
    temp_time = float(temp_time) # 如果是整数，转成浮点型
    if(len(str(temp_time).split('.')[1]) > 3):
        temp_time = round(temp_time, 3) # 保留小数点后面三位
    print('小数:{}'.format(temp_time))

    fen = math.floor(temp_time / 60) # 分钟
    miao = math.floor(temp_time - fen * 60) # 秒钟
    haomiao  = int((temp_time - fen * 60 - miao) * 1000) # 毫秒
    fen = str(fen)
    miao = str(miao)
    haomiao = str(haomiao)
    if(len(fen) < 2):
        fen = '0' + str(fen)
    if(len(miao) < 2):
        miao = '0' + str(miao)
    if(len(haomiao) == 1):
        haomiao = '00' + haomiao
    if(len(haomiao) == 2):
        haomiao = '0' + haomiao
    print("fen:{}".format(fen))
    print("miao:{}".format(miao))
    print("haomiao:{}".format(haomiao))
    print('final time : {}'.format(fen + ":" + miao + '.' + haomiao))
    final_time = fen + ":" + miao + '.' + haomiao
    return final_time

# 把帧转化为首次出现的时间
def get_words_time(rate, words_block_list):
    content_s = ''
    final_words_blcok_list = []
    for words_block in words_block_list:
        str = ''
        for words in words_block["words"]:
            str += words['content']
            str += '|'
        if str == content_s:
            continue
        else:
            content_s = str
            words_block["time"] = transfer_time(words_block["time"] / rate)
            final_words_blcok_list.append(words_block)
    return final_words_blcok_list



@app.get("/run")
def get_1():
    return {"status":"ok"}

@app.post("/api/pdfocr")
def pdfocr(file: bytes = File(...)):
    try:
        docs = fitz.open(stream = file, filetype="pdf")
    except RuntimeError:
        return pack_error_json("请检查PDF文件，文件错误或者不是PDF文件")
    zoom = 2 # to increase the resolution
    mat = fitz.Matrix(zoom, zoom)
    output_list = list()
    idx = 0
    for page in docs:
        pix = page.getPixmap(matrix = mat)
        data = pix.tobytes()
        decoded = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
        re = ocr.chi_sim_OCR(decoded)
        output_list.append(re)
        idx = idx + 1
    return get_pdf_ocr_return_json("2000","success",output_list)

@app.post("/api/voice2word")
def voice2word(file: UploadFile = File(...)):
    # test the file is wav format or not:
    file_copy = copy.deepcopy(file)
    if file_copy.file.read()[0:4] != b'RIFF':
        return pack_error_json("不是 wav 类型文件，请重新上传")
    print(file_copy.file.read()[0:4])
    print(file_copy.file.read()[0:4] == b'RIFF')
    try:
        result = voiceOCR(file)
    except ValueError:
        return pack_error_json("Wav 文件类型不正确，文件编码不能是pcm,aiff/aiff-c,FLAC")
    return get_voice_2_word_return_json("2000","OK",result)

@app.post("/api/videoocr")
def videoocr(video_file: UploadFile=File(...), config:str=Form(...)):
    try:
        # save video file
        file_bytes = video_file.file.read()
        for i in os.listdir('./'):
            if(i.find("rev_video")>=0):
                os.remove(os.path.join('./', i))
                print("delete finish......")
                break
        with open("./rev_video.mp4", 'wb') as f:
            f.write(file_bytes)
        print("save video finish......")
        
        # 文件类型
        kind = filetype.guess("./rev_video.mp4")
        if kind.MIME == "video/mp4":
            print('视频格式正确')
        else:
            print(kind.MIME)
            wrong_data = []
            return pack_json(code=6000, data=wrong_data)
        # 帧率
        cap = cv2.VideoCapture("./rev_video.mp4")
        rate = cap.get(5)
        print("video:{} fps".format(rate))

        # get rectangle location
        config_json = json.loads(config)
        # length
        location_length = len(config_json["rectangle_location"])
        print("location_length: {}".format(location_length))
        rectangle_location_1 = config_json["rectangle_location"][0]["cor"]
        if location_length == 2:
            rectangle_location_2 = config_json["rectangle_location"][1]["cor"]
        words_block_list_1=[]
        if location_length == 2:
            words_block_list_2=[]
        data = []
        frame_num = 0
        while cap.isOpened():
            frame_num += 1
            ret, frame = cap.read()
            if(ret):
                frame_rectangle_1 = frame[rectangle_location_1[0][1]:rectangle_location_1[1][1],rectangle_location_1[0][0]:rectangle_location_1[1][0]]
                print(frame_rectangle_1.shape)
                if location_length == 2 :
                    frame_rectangle_2 = frame[rectangle_location_2[0][1]:rectangle_location_2[1][1],rectangle_location_2[0][0]:rectangle_location_2[1][0]]
                    print(frame_rectangle_2.shape)
                re_list_1 = ocr.chi_sim_OCR(frame_rectangle_1)
                words_1 = get_words(re_list_1)
                words_block_list_1.append({"time":frame_num, "words":words_1})
                if location_length == 2:
                    re_list_2 = ocr.chi_sim_OCR(frame_rectangle_2)
                    words_2 = get_words(re_list_2)
                    words_block_list_2.append({"time":frame_num, "words":words_2})
            else:
                break
        final_words_block_list_1 = get_words_time(rate, words_block_list_1)
        data.append({"rectangle_id":1, "words_blcok_list":final_words_block_list_1})
        if location_length == 2:
            final_words_block_list_2 = get_words_time(rate, words_block_list_2)
            data.append({"rectangle_id":2, "words_blcok_list":final_words_block_list_2})
        return_json = pack_json(code = 2000, data = data)
    except:
        wrong_data = []
        return_json = pack_json(code= 4000, data= wrong_data)
    return return_json

@app.post("/api/videocheck")
def videocheck(video_file: UploadFile=File(...), config:str=Form(...)):
    file_bytes = video_file.file.read()

    if filetype.guess(file_bytes).MIME != "video/mp4":
        return pack_error_json("视频类型不对，请重新上传文件类型")
        
    
    for node in os.listdir("./"):
        if(node.find("rev_video")>=0):
            os.remove(os.path.join("./",node))
            break
    
    with open("./rev_video.mp4","wb") as f:
        f.write(file_bytes)

    config_json = json.loads(config)
    rectangle_location = config_json["rectangle_location"]    
    cap = cv2.VideoCapture("./rev_video.mp4")
    ret, frame = cap.read()
    cap.release()

    if ret :
        for each in rectangle_location:
            x1,y1,x2,y2 = each["cor"][0][0],each["cor"][0][1],each["cor"][1][0],each["cor"][1][1]
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
    else :
        return pack_error_json("视频损坏")

    success,encoded_image = cv2.imencode(".jpg",frame)
    img_bytes = encoded_image.tostring()
    
    outcome = {
        "content":{
            "code" :2000,
            "message" : "success"
        }
    }

    header = { 
        "outcome" : json.dumps(outcome)
    }
    
    return StreamingResponse(io.BytesIO(img_bytes),media_type="image/jpeg",headers=header)

@app.get("/")
def return_index(request:Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request":request
        }
    )


app.mount("/",StaticFiles(directory="/root/static"),name="/")


import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0" , port=8800, reload=True)
    
