import math
import re
from datetime import datetime

MIN_CLAVE = 14
MAX_CLAVE_BYTES = 72
patronUsuario = r"[A-Za-z0-9_.\-]{4,20}"
patronNombre = r"[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:[ '\-][A-Za-zÁÉÍÓÚáéíóúÑñ]+)*"
patronTelefono = r"(?:\+?56)?[2-9]\d{8}"
patronCorreo = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}"

def validar_nombre(texto, campo="nombre"):
    valor = (texto or "").strip()
    if not valor:
        return f"El {campo} es obligatorio."
    if not re.fullmatch(patronNombre, valor):
        return f"El {campo} solo puede contener letras."
    return None

def validar_telefono(texto):
    valor=(texto or "").strip()
    if not re.fullmatch(patronTelefono, valor):
        return "El telefono debe contener solo numeros (ej: +56912345678)"
    return None

def validar_correo(texto):
    valor = (texto or "").strip()
    if not re.fullmatch(patronCorreo, valor):
        return "El correo electrónico no tiene un formato válido"
    return None

def validar_usuario(texto):
    valor = (texto or "").strip()
    if not re.fullmatch(patronUsuario, valor):
        return "El usuario debe tener de 4 a 20 caracteres (letras, números, _ . -)."
    return None

def validar_salario(texto):
    try:
        num = float((texto or "").strip())
    except ValueError:
        return "El salario debe ser un número válido."
    if not math.isfinite(num) or num < 0:
        return "El salario debe ser un número finito no negativo."
    return None

def validar_clave(clave):
    if not isinstance(clave, str) or not clave.strip() or "\x00" in clave:
        return "La contraseña no es válida."
    if len(clave) < MIN_CLAVE:
        return f"La contraseña debe tener al menos {MIN_CLAVE} caracteres."
    if len(clave.encode("utf-8")) > MAX_CLAVE_BYTES:
        return f"La contraseña no puede superar los {MAX_CLAVE_BYTES} bytes."
    return None

def validar_fecha_iso(texto, campo="fecha"):
    fecha_txt = (texto or "").strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha_txt):
        return None, f"La {campo} debe tener formato AAAA-MM-DD."
    try:
        fecha_dt = datetime.strptime(fecha_txt, "%Y-%m-%d").date()
    except ValueError:
        return None, f"La {campo} no es una fecha válida."
    return (fecha_txt, fecha_dt), None

# --- NOTAS DETALLADAS DEL ARCHIVO (VALIDACIONES CENTRALIZADAS) ---
# Por que existe este archivo: centraliza todas las reglas de formato en un solo lugar para que tanto las Vistas (validacion inmediata campo a campo) como los Controladores (barrera de seguridad) usen exactamente los mismos criterios sin duplicar codigo.
# - validar_nombre(texto, campo): exige texto no vacio y solo letras/acentos/espacios/guion/apostrofe (patronNombre), bloqueando numeros o simbolos en nombres de personas.
# - validar_telefono(texto): usa patronTelefono = (?:\+?56)?[2-9]\d{8} para aceptar solo telefonos chilenos de 9 digitos (celulares o fijos) con +56 o 56 opcional.
# - validar_correo(texto): verifica formato usuario@dominio.ext mediante patronCorreo.
# - validar_usuario(texto): valida usernames de 4 a 20 caracteres (letras, numeros, _, ., -) con patronUsuario.
# - validar_salario(texto): convierte a float y usa math.isfinite() para bloquear textos, NaN, Infinito o salarios negativos.
# - validar_clave(clave): rechaza vacios o byte nulo (\x00), exige minimo 14 caracteres (MIN_CLAVE) y maximo 72 bytes UTF-8 (MAX_CLAVE_BYTES) porque bcrypt trunca silenciosamente claves mayores a 72 bytes.
# - validar_fecha_iso(texto, campo): combina regex ^\d{4}-\d{2}-\d{2}$ (formato estricto AAAA-MM-DD) + datetime.strptime (fecha real del calendario) y retorna ((texto, date), None) para permitir comparaciones cronologicas entre fechas.

