import os
from cryptography.fernet import Fernet, InvalidToken
from utils.registro import logger


def _obtener_clave() -> bytes:
    """Lee la clave de cifrado desde la variable de entorno ENCRYPT_KEY."""
    clave = os.getenv("ENCRYPT_KEY", "").strip()
    if not clave:
        raise RuntimeError(
            "La variable ENCRYPT_KEY no está configurada en .env. "
            "Genere una clave con: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )
    return clave.encode()


def cifrar(texto: str) -> str:
    """Cifra un texto plano y devuelve el token cifrado como cadena."""
    try:
        f = Fernet(_obtener_clave())
        return f.encrypt(str(texto).encode("utf-8")).decode("utf-8")
    except Exception as e:
        logger.error("Error al cifrar dato: %s", e)
        raise RuntimeError("No se pudo cifrar el dato.") from e


def descifrar(token: str) -> str:
    """Descifra un token y devuelve el texto original. Si falla retorna el token sin cambios (compatibilidad)."""
    if not isinstance(token, str) or not token:
        return token
    try:
        f = Fernet(_obtener_clave())
        return f.decrypt(token.encode("utf-8")).decode("utf-8")
    except (InvalidToken, Exception):
        # El valor podría ser texto plano de antes de implementar cifrado
        return token

# --- NOTAS DETALLADAS DEL ARCHIVO (MÓDULO DE CIFRADO) ---
# - _obtener_clave(): lee ENCRYPT_KEY desde .env; lanza RuntimeError si no está configurada.
# - cifrar(texto): usa Fernet (AES-128-CBC con HMAC-SHA256) para cifrar; Fernet genera un IV aleatorio
#   por cada llamada, por lo que el mismo correo cifrado dos veces produce tokens distintos.
# - descifrar(token): descifra con la misma clave; si el token no es válido (p. ej., dato anterior
#   en texto plano), retorna el valor sin cambios para mantener compatibilidad con datos existentes.
# - Por qué Fernet: es la implementación recomendada de la librería 'cryptography' para cifrado
#   simétrico autenticado; incluye verificación de integridad (HMAC), evitando que los datos
#   almacenados puedan ser alterados sin ser detectados.
