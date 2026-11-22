import os
from utils.registro import logger
import json
import urllib.request
import urllib.error
import http.client
import time
import math

# fuentes en orden: si la primera falla, se prueba la segunda
API_PRINCIPAL = os.getenv("API_URL_PRINCIPAL", "https://mindicador.cl/api")
API_RESPALDO = os.getenv("API_URL_RESPALDO", "https://findic.cl/api")
try:
    API_TIMEOUT = max(1, int(os.getenv("API_TIMEOUT", "10")))
except ValueError:
    API_TIMEOUT = 10

FUENTES = (
    ("mindicador.cl", API_PRINCIPAL),
    ("findic.cl", API_RESPALDO),
)


class ErrorAPI(Exception):
    """Se lanza cuando la API falla."""


class ErrorRed(ErrorAPI):
    """No hay conexión o se agotó el tiempo."""


class ErrorHTTP(ErrorAPI):
    """La API devolvió error 4xx o 5xx."""
    def __init__(self, codigo, mensaje):
        super().__init__(mensaje)
        self.codigo = codigo


class ErrorFormato(ErrorAPI):
    """La respuesta no tiene la estructura esperada."""


class ServicioIndicadores:
    REINTENTOS = 2

    def __init__(self):
        self.fuente_usada = None

    def __pedir_json(self, url):
        solicitud = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "EcoTech-Sistema/1.0",
        })
        ultimo_error = None
        for intento in range(self.REINTENTOS + 1):
            try:
                with urllib.request.urlopen(solicitud, timeout=API_TIMEOUT) as respuesta:
                    cuerpo = respuesta.read()
                break  # lectura exitosa; salir del bucle
            except urllib.error.HTTPError as e:
                # HTTPError va ANTES que URLError (hereda de ella)
                if e.code == 404:
                    raise ErrorHTTP(404, "No hay datos para esa consulta.") from e
                if e.code == 429 or e.code >= 500:
                    # error temporal: esperar y reintentar
                    ultimo_error = ErrorHTTP(e.code, "El servicio está ocupado o no disponible.")
                    time.sleep(2 ** intento)
                    continue
                raise ErrorHTTP(e.code, "La solicitud fue rechazada.") from e
            except (urllib.error.URLError, TimeoutError,
                    http.client.HTTPException, OSError) as e:
                # incluye RemoteDisconnected, IncompleteRead, errores de socket
                ultimo_error = ErrorRed("No hay conexión con el servicio.")
                time.sleep(2 ** intento)
        else:
            # el bucle agotó todos los intentos sin break
            raise ultimo_error
        try:
            return json.loads(cuerpo.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ErrorFormato("La respuesta no es JSON válido.") from e

    def __limpiar(self, datos):
        """Valida la estructura del JSON y deja solo los campos necesarios."""
        if not isinstance(datos, dict) or not isinstance(datos.get("serie"), list):
            raise ErrorFormato("La respuesta no tiene el formato esperado.")
        serie = []
        for item in datos["serie"]:
            try:
                valor = float(item["valor"])
                fecha = str(item["fecha"])[:10]
            except (KeyError, TypeError, ValueError):
                continue
            if math.isfinite(valor) and valor > 0:
                serie.append({"fecha": fecha, "valor": valor})
        return {
            "nombre": datos.get("nombre", ""),
            "unidad_medida": datos.get("unidad_medida", ""),
            "serie": serie,
        }

    def consultar(self, ruta):
        """Prueba cada fuente en orden; si una falla pasa a la siguiente sin mostrar errores técnicos."""
        ultimo_error = None
        for nombre, base in FUENTES:
            try:
                datos = self.__pedir_json(f"{base}/{ruta}")
                self.fuente_usada = nombre
                return datos
            except ErrorAPI as e:
                logger.error("Fallo consultando fuente %s (%s): %s", nombre, ruta, e)
                ultimo_error = e
        # todas las fuentes fallaron
        raise ultimo_error

    def ultimos_valores(self, indicador):
        return self.__limpiar(self.consultar(indicador))

    def valor_en_fecha(self, indicador, fecha):
        return self.__limpiar(self.consultar(f"{indicador}/{fecha}"))

    def serie_anual(self, indicador, anio):
        return self.__limpiar(self.consultar(f"{indicador}/{anio}"))

# --- NOTAS DETALLADAS DEL ARCHIVO (SERVICIO DE INDICADORES API) ---
# - Variables API_PRINCIPAL, API_RESPALDO y API_TIMEOUT leídas desde .env con try/except ValueError y max(1,...).
# - Jerarquía ErrorAPI -> ErrorRed / ErrorHTTP / ErrorFormato para distinguir tipo de fallo.
# - __pedir_json: captura HTTPError ANTES que URLError; también captura http.client.HTTPException y OSError
#   para cubrir RemoteDisconnected e IncompleteRead. Reintenta con backoff exponencial solo en errores temporales.
# - consultar: recorre FUENTES (mindicador.cl → findic.cl); si la principal falla registra en log y prueba el respaldo.
#   El usuario NUNCA ve el traceback ni el detalle técnico.
# - ultimos_valores / valor_en_fecha / serie_anual: arman la ruta y retornan datos ya saneados por __limpiar.
