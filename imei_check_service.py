import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("CHECK_IMEI_API_TOKEN")

# Реализация функции для работы с API imeicheck
def check_imei(imei: str):
    url = "https://api.imeicheck.net/v1/checks"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept-Language": "en",
        "Content-Type": "application/json"
    }
    data = {
        "deviceId": imei,
        "serviceId": 12     
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
