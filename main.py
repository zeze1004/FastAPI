from typing import Optional

from fastapi import FastAPI, status, HTTPException, APIRouter
from pydantic import BaseModel # 사용자가 정의한 클래스를 annotation해서 쓸 수 있음
import json

app = FastAPI()

@app.get("/")
def root():
    return "Hello World"

@app.get("/health")
def healthcheck():
    return 'healthy'