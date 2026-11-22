ADMINISTRADOR = "ADMINISTRADOR"
GERENTE = "GERENTE"
EMPLEADO = "EMPLEADO"
RRHH = "RRHH"
ROLES = (ADMINISTRADOR, GERENTE, EMPLEADO, RRHH)


def normalizar_rol(rol):
    valor = str(rol).strip().upper()
    equivalencias = {
        "ADMIN": ADMINISTRADOR,
        "ADMINISTRADOR": ADMINISTRADOR,
        "GERENTE": GERENTE,
        "EMPLEADO": EMPLEADO,
        "OPERATIVO": EMPLEADO,
        "RRHH": RRHH,
        "RECURSOS HUMANOS": RRHH,
    }
    if valor not in equivalencias:
        raise ValueError("El rol debe ser Administrador, Gerente, RRHH o Empleado.")
    return equivalencias[valor]

# --- NOTAS GENERALES DEL ARCHIVO (ROLES) ---
# - Define las constantes oficiales de rol: ADMINISTRADOR, GERENTE, RRHH y EMPLEADO.
# - normalizar_rol(): limpia espacios y mayusculas y traduce sinonimos (ADMIN, OPERATIVO, RECURSOS HUMANOS) a un rol oficial; si llega un rol desconocido lanza ValueError.

