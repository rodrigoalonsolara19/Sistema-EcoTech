import json
from datetime import date
from conex.conn import ConexionBD
from utils.registro import logger
from sqlite3 import Error


class DAOIndicadores:
    """Persiste el historial de consultas a la API de indicadores en la tabla consultaindicador."""

    def __init__(self):
        self.__conexion_provider = ConexionBD()

    def guardar_consulta(self, indicador: str, tipo: str, parametro: str,
                         fuente: str, resultado: list) -> bool:
        """Inserta un registro de la consulta realizada a la API."""
        sql = """
            INSERT INTO consultaindicador
                (fechaConsulta, indicador, tipoConsulta, parametro, fuente, resultado)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (
                str(date.today()),
                indicador,
                tipo,
                parametro,
                fuente,
                json.dumps(resultado, ensure_ascii=False),
            ))
            conexion.commit()
            return True
        except Error as e:
            logger.error("Error al guardar consulta de indicador: %s", e)
            return False
        finally:
            conexion.close()

    def listar_historial(self) -> list[dict]:
        """Retorna el historial completo de consultas a la API."""
        sql = """
            SELECT idConsulta, fechaConsulta, indicador, tipoConsulta,
                   parametro, fuente, resultado
            FROM consultaindicador
            ORDER BY idConsulta DESC
        """
        historial = []
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            return historial
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            for fila in cursor.fetchall():
                try:
                    serie = json.loads(fila[6])
                except (json.JSONDecodeError, TypeError):
                    serie = []
                historial.append({
                    "id": fila[0],
                    "fecha": fila[1],
                    "indicador": fila[2],
                    "tipo": fila[3],
                    "parametro": fila[4],
                    "fuente": fila[5],
                    "serie": serie,
                })
            return historial
        except Error as e:
            logger.error("Error al listar historial de indicadores: %s", e)
            return []
        finally:
            conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (DAO INDICADORES) ---
# - guardar_consulta(): persiste en consultaindicador la fecha de hoy, el indicador, tipo de consulta
#   (actuales/fecha/anio), parámetro usado, fuente API que respondio y la serie de datos como JSON.
# - listar_historial(): recupera todos los registros en orden descendente y deserializa el campo resultado.
