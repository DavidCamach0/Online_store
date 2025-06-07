# Escritorio/GIT/backend/service/token_service.py

from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv
load_dotenv()
serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

def generar_token(email: str) -> str:
    return serializer.dumps(email)

def verificar_token(token: str, max_age=3600) -> str:
    from itsdangerous import BadSignature, SignatureExpired
    try:
        email = serializer.loads(token, max_age=max_age)
        return email
    except (BadSignature, SignatureExpired):
        return None
