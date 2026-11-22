import os
from pathlib import Path
def cargar_env(ruta_env=None):
    archivo = Path(ruta_env) if ruta_env else Path(__file__).resolve().parent.parent / ".env"
    if not archivo.is_file():
        return
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))

# --- NOTAS DETALLADAS DEL ARCHIVO (CARGADOR .ENV) ---
# - cargar_env(ruta_env=None): se creo para leer variables de configuracion desde .env usando solo libreria estandar (pathlib y os), evitando depender de paquetes externos como python-dotenv.
# - Si .env no existe, retorna en silencio para que el sistema siga funcionando con los valores por defecto.
# - Ignora lineas vacias, comentarios (#) y lineas sin '=', separa solo en el primer '=' (split('=', 1)) por si un valor trae '=' adentro, limpia espacios/comillas y usa os.environ.setdefault() para no pisar variables ya configuradas en el sistema operativo.
