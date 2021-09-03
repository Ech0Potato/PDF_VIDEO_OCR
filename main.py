from fastapi import FastAPI, Form
from pydantic import BaseModel
app = FastAPI()

class pdfItem(BaseModel):
    pdf_file : str

@app.get("/run")
def get_1():
    return {"status":"ok"}

@app.post("/api/pdfocr")
def pdfocr(args:pdfItem):
    print(len(args.pdf_file))
    return {"status":"ok"}