import asyncio
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from tg_bot import is_valid_imei
from fastapi.security import APIKeyHeader
from imei_check_service import check_imei
from pydantic import BaseModel
from dotenv import load_dotenv
from tg_bot import run_bot
from db import init_db
import os


app = FastAPI()
load_dotenv()
# Т.к. задача тестовая реализовал хранение токенов в .env, в дальнейшем можно развернуть хранение в БД с динамической
# генерацией
API_TOKENS = [
    os.getenv("API_TOKEN_1"),
    os.getenv("API_TOKEN_2")
]

api_key_header = APIKeyHeader(name="token", auto_error=False)


# Проверка на то, указан верный API токен или нет
def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in API_TOKENS:
        raise HTTPException(status_code=401, detail=f"Invalid API key: {api_key}")
    return api_key

# Сформировал класс для простого хранения тела запроса
class IMEIRequest(BaseModel):
    imei: str
    token: str


@app.get("/")
def read_root():
    return {"message": "IMEI Checker API is running!"}


@app.post("/api/check-imei")
async def check_imei_api(request: IMEIRequest, api_key: str = Depends(api_key_header)):
    if not is_valid_imei(request.imei):
        raise HTTPException(status_code=400, detail="Некорректный IMEI")
    
    try:
        result = check_imei(request.imei)
        return {"imei": request.imei, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при проверке IMEI: {e}")


async def run_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    init_db()

    api_task = asyncio.create_task(run_api())
    bot_task = asyncio.create_task(run_bot())

    await asyncio.gather(api_task, bot_task)

if __name__ == "__main__":

    asyncio.run(main())