# Short Description

an http-api pdf, voice, video OCR format backend written in Python with PaddleOCR moudle and FastAPI. 

# ENV init

**Consier start a container from a docker image first**:

```bash
docker run -itd -p <host_port>:8800 ech0potato/sansan:v0.7 /bin/bash /root/start.sh 
```
then you can direct to API document to try this backend program.

**If you want to configure envrionment yourself:**

ubuntu 18.04 or ubuntu 18.04 +
Python 3.7 ( Recommended ) , other version might get paddleOCR Error with unknown reason. 

```bash
$ apt install libgl1-mesa-glx  libpulse-dev libasound2-dev python-all-dev build-essential swig 
$ pip install fastapi opencv-python paddlepaddle paddleocr wheel speechrecognition fitz pocketsphinx PyMuPDF filetype
```
