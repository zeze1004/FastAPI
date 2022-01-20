from fastapi import FastAPI, status

app = FastAPI()

@app.get("/")
def main():
    return "main page"

initial_data = {'params': 'ok'}
example_params = {}
def init():
    # 서버를 사용할 수 있게 초기 데이터를 어디선가 가져오는 로직
    # db나 redis등 서버에 연결한다.
   # -> ingress gateway에게 내(서버)가 건강하다(200 ok)를 보내주는 역할
    if initial_data:
        return True
    return False

@app.get("/health") # /health: health-check endpoint
def health():
    # 내(서버)가 괜찮다는걸 istio에게 보내줌
    if init():
        return "200 OK"
    else:
        return "500 Internal Server Error"

@app.get("/print/{somePath}")
def somePath(somePath: str):
    return somePath

@app.get("/print/", status_code=201)
async def printing(params: str):
    return {"params": params}

@app.get("/input_params")
def input_params():
    try:
        if example_params:
            return health()
    except:
        return "wrong params"



