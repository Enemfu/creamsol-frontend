import os
from dotenv import load_dotenv
load_dotenv()

API_BASE_URL = os.getenv("CREAMSOL_API_URL", "http://localhost:8000")
SENHA_INTERMEDIARIO = os.getenv("SENHA_INTERMEDIARIO", "")
TOKEN_PROFISSIONAL   = os.getenv("TOKEN_PROFISSIONAL", "")