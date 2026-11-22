import logging

logging.basicConfig(
    filename="errores.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger("ecotech")

# --- NOTAS DETALLADAS DEL ARCHIVO (REGISTRO DE ERRORES / LOGGING) ---
# - logging.basicConfig(...): configura un archivo errores.log en UTF-8 con fecha/hora, nivel (ERROR/WARNING) y mensaje.
# - logger = logging.getLogger("ecotech"): instancia compartida por DAOs, servicios, conexion y vistas; se agrego para guardar el detalle tecnico real para depurar sin exponer stacktraces ni rutas internas en la pantalla del usuario.
