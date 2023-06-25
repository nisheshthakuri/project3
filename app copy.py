from fastapi import FastAPI,UploadFile,File
import requests
import os
import re
from fastapi.middleware.cors import CORSMiddleware
import easyocr

app = FastAPI()

# Define CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ocrImage(img):
    values=[]
    reader = easyocr.Reader(['hi'])
    result = reader.readtext(img)
    for detection in result: 
        text = detection[1]
        values.append(text)
    return values

@app.post("/uploadimage/")
async def upload_image(image: UploadFile = File(...)):
    image_bytes = await image.read()
    with open(image.filename, "wb") as f:
        f.write(image_bytes)
    return {image.filename}

@app.get("/detection")
async def detect_image(image_url):
    result=ocrImage(image_url)
    return {"message": result} 
