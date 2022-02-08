# Short Description

an http-api pdf, voice, video OCR format backend written in Python with PaddleOCR moudle and FastAPI. 

# ENV init

**Consier start a container from a docker image first**:

```bash
$ docker run -itd -p <host_port>:8800 ech0potato/sansan:v0.7 /bin/bash /root/start.sh 
```
then you can direct to API document to try this backend program.

**If you want to configure the envrionment yourself:**

ubuntu 18.04 or ubuntu 18.04 +
Python 3.7 ( Recommended ) , other version might get paddleOCR Error with unknown reason. 

```bash
$ apt install libgl1-mesa-glx  libpulse-dev libasound2-dev python-all-dev build-essential swig 
$ pip install fastapi opencv-python paddlepaddle paddleocr wheel speechrecognition fitz pocketsphinx PyMuPDF filetype
```

## Start ( if you configured the envrionment yourself )

```bash
# change directory to the root of this project.
$ python3 main.py
```

the RESTAPI backend will listen at `localhost:8800` by default.

# API Details

## PDF OCR

**Request:**
```
URL: http://domain:port/api/pdfocr
METHOD: POST
Content-Type: application/pdf

Input Example:

"pdf_file":raw_pdf_bytes

```

**Response:**
```json
{
"code" : 2000,
"message": "success",
"data":[
{
"page": 1,
"words_block_list":[
{
"words": "第一行文字",
"location":[
[10, 10],
[100,20]
]
},
{
"words": "第二行文字",
"location":[
[10, 20],
[100,30]
]
}
] 
},
{
"page": 2,
"words_block_list":[
{
"words": "第一行文字",
"location":[
[10, 10],
[100,20]
]
},
{
"words": "第二行文字",
"location":[
[10, 20],
[100,30]
]
}
] 
}
]
}

```
## 
