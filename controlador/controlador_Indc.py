from controlador.controlador_base import ControladorBase
from servicio.servicio_indicadores import (ServicioIndicadores, ErrorAPI, ErrorRed, ErrorHTTP, ErrorFormato)
from utils import validador_api as validador
from dao.dao_indicadores import DAOIndicadores


class ControladorIndicadores(ControladorBase):
    def __init__(self):
        super().__init__()
        self.__servicio = ServicioIndicadores()
        self.__dao = DAOIndicadores()

    @property
    def fuente_usada(self):
        return self.__servicio.fuente_usada

    def _exige_autenticado(self):
        if self._usuario_actual() is None:
            raise PermissionError("Debe iniciar sesión para consultar indicadores.")

    def __ejecutar(self, indicador, consulta, tipo_consulta, parametro=""):
        """Exige sesión, valida el indicador, ejecuta la consulta y guarda en BD."""
        try:
            self._exige_autenticado()
            codigo, error = validador.validar_indicador(indicador)
            if error:
                return None, error
            datos = consulta(codigo)
            # Persistir en la base de datos
            try:
                self.__dao.guardar_consulta(
                    indicador=codigo,
                    tipo=tipo_consulta,
                    parametro=parametro,
                    fuente=self.__servicio.fuente_usada or "",
                    resultado=datos.get("serie", []),
                )
            except Exception:
                pass  # guardar en BD es secundario; no interrumpe la consulta
            return datos, "Consulta exitosa."
        except PermissionError as e:
            return None, str(e)
        except ErrorAPI as e:
            return None, self.__mensaje_error(e)
        except Exception:
            return None, "Ocurrió un error inesperado al consultar el servicio."

    def consultar_actuales(self, indicador):
        return self.__ejecutar(
            indicador,
            lambda cod: self.__servicio.ultimos_valores(cod),
            tipo_consulta="actuales",
        )

    def consultar_fecha(self, indicador, fecha):
        fecha_ok, error = validador.validar_fecha(fecha)
        if error:
            return None, error
        return self.__ejecutar(
            indicador,
            lambda cod: self.__servicio.valor_en_fecha(cod, fecha_ok),
            tipo_consulta="fecha",
            parametro=fecha_ok,
        )

    def consultar_anio(self, indicador, anio):
        anio_ok, error = validador.validar_anio(anio)
        if error:
            return None, error
        return self.__ejecutar(
            indicador,
            lambda cod: self.__servicio.serie_anual(cod, anio_ok),
            tipo_consulta="anio",
            parametro=anio_ok,
        )

    def convertir_monto(self, monto_texto):
        try:
            self._exigir_gerente()
            monto, error = validador.validar_monto(monto_texto)
            if error:
                return None, error
            conversion = {}
            for codigo in ("uf", "dolar", "euro", "utm"):
                serie = self.__servicio.ultimos_valores(codigo)["serie"]
                if not serie:
                    return None, f"No hay valor disponible para {codigo.upper()}."
                conversion[codigo] = monto / serie[0]["valor"]
            return conversion, "Conversión realizada."
        except PermissionError as e:
            return None, str(e)
        except ErrorAPI as e:
            return None, self.__mensaje_error(e)
        except Exception:
            return None, "Ocurrió un error inesperado al convertir el monto."

    def listar_historial(self):
        """Retorna el historial de consultas guardadas en la BD."""
        return self.__dao.listar_historial()

    def __mensaje_error(self, e):
        if isinstance(e, ErrorHTTP):
            return str(e)
        if isinstance(e, ErrorRed):
            return "No hay conexión con el servicio. Intente más tarde."
        if isinstance(e, ErrorFormato):
            return "El servicio devolvió datos no válidos."
        return "No fue posible consultar el servicio externo."

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR DE INDICADORES API) ---
# - Ahora guarda cada consulta exitosa en consultaindicador via DAOIndicadores.guardar_consulta().
# - __ejecutar: captura también Exception genérica para evitar que cualquier error imprevisto muestre
#   un traceback al usuario; en su lugar muestra un mensaje amigable.
# - convertir_monto: solo para Gerente/Admin; captura Exception genérica igual.
# - listar_historial(): expone el historial persistido en SQLite.
# - __mensaje_error: traduce ErrorHTTP/ErrorRed/ErrorFormato a mensajes amigables.
