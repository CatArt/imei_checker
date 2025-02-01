from dotenv import load_dotenv
import os

load_dotenv()

API_TOKENS = [
    os.getenv("API_TOKEN_1"),
    os.getenv("API_TOKEN_2")
]

if "4321" not in API_TOKENS:
    print(False)
else:
    print(True)