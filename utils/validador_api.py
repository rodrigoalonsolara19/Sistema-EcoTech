# re sirve para revisar formatos (por ejemplo, que la fecha tenga forma 15-03-2024).
import re
# date y datetime sirven para trabajar con fechas.
from datetime import date, datetime
import math

INDICADORES_PERMITIDOS = {
    "uf": "Unidad de Fomento",
    "utm": "Unidad Tributaria Mensual",
    "dolar": "Dolar",
    "euro": "Euro"
    }

# Funcion para limpiar el diccionario
def sanear_texto(texto):
    """QUITA ESPACIOS Y PASA A MINUSCULAS"""
    return texto.strip().lower()

def validar_indicador(texto):
    """Retorna (codigo, error) si todo está bien, error es None"""
    codigo = sanear_texto(texto)
    if codigo not in INDICADORES_PERMITIDOS:
        return None, "Indicador no permitido."
    
    return codigo, None

def validar_fecha(texto):
    fecha_txt = sanear_texto(texto)
    if not re.match(r"^\d{2}-\d{2}-\d{4}$", fecha_txt): 
        return None, "Use el formato DD-MM-AAAA"
# El re.match exige exactamente dd-mm-aaaa
# strptime falla si pones algo como 31-02-2024
    try:
        fecha = datetime.strptime(fecha_txt, "%d-%m-%Y").date()
    except ValueError:
        return None, "Esa fecha no existe"
    if fecha > date.today():
        return None, "No puedes usar fechas futuras"
    if fecha < date(1990, 1, 1):
        return None, "La fecha debe ser desde 1990 en adelante"
    return fecha_txt, None

def validar_anio(texto):
    anio_txt = sanear_texto(texto)
    if not re.match(r"^\d{4}$", anio_txt):
        return None, "Use solo 4 dígitos para el año"
    anio = int(anio_txt)
    if anio < 1990 or anio > date.today().year:
        return None, "Año fuera de rango"
    return anio_txt, None

# Validar el monto

def validar_monto(texto):
    try:
        monto = float(sanear_texto(texto).replace(",", "."))
    except ValueError:
        return None, "El monto debe ser un número."
    if not math.isfinite(monto) or monto <= 0:
        return None, "El monto debe ser un número mayor que cero."
    if monto > 1_000_000_000_000:
        return None, "El monto es demasiado grande"
    return monto, None

# --- NOTAS DETALLADAS DEL ARCHIVO (VALIDADOR DE API) ---
# Por que existe este archivo: valida y sanea toda entrada del usuario ANTES de construir la URL o consultar la API externa, evitando peticiones inutiles, errores de formato o manipulacion de rutas.
# - INDICADORES_PERMITIDOS: diccionario de lista blanca (uf, utm, dolar, euro); cualquier otro texto queda bloqueado.
# - sanear_texto(texto): quita espacios laterales y convierte a minusculas (.strip().lower()) antes de validar.
# - validar_indicador(texto): comprueba que el codigo saneado exista en INDICADORES_PERMITIDOS.
# - validar_fecha(texto): exige DD-MM-AAAA exacto (regex), verifica que la fecha exista en el calendario (datetime.strptime, bloqueando 31-02-2024) y limita el rango entre 1990-01-01 y hoy (sin fechas futuras).
# - validar_anio(texto): exige exactamente 4 digitos (\d{4}) entre 1990 y el anio actual.
# - validar_monto(texto): acepta punto o coma decimal, verifica con math.isfinite() que no sea NaN ni Infinito, que sea > 0 y menor o igual a 1_000_000_000_000.


