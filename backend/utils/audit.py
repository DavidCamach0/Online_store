# /Escritorio/GIT/backend/utils/audit.py

from backend.core.database import get_cursor
from fastapi import Request
import datetime
from typing import Optional
# Registrar el error en logs, pero no interrumpir la operación principal
from backend.utils.logger import get_logger
logger = get_logger(__name__)



def registrar_auditoria(
    usuario_id: Optional[int],
    accion: str,
    request: Request
) -> None:
    try:
        endpoint = request.url.path
        metodo = request.method
        ip = request.client.host
        user_agent = str(request.headers.get("user-agent","Desconocido"))
        with get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO auditoria (usuario_id, accion, metodo,endpoint,user_agent, ip)
                VALUES (%s, %s, %s, %s, %s,%s)
                """,
                (usuario_id, accion, metodo,endpoint,user_agent, ip)
            )
    except Exception as e:
        
        logger.error(f"Error al registrar auditoría: {e}")
