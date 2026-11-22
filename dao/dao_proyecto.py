from conex.conn import ConexionBD
from modelo.proyecto import Proyecto
from utils.registro import logger
from sqlite3 import Error

class DAOProyecto:
    def __init__(self):
        self.__conexion_provider = ConexionBD()

    def registrar(self, proy: Proyecto) -> bool:
        sql = "INSERT INTO proyecto (nomProy, fechaInicio, fechaFin, estado) VALUES (?, ?, ?, ?)"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (proy.nomProy, proy.fechaInicio, proy.fechaFin, proy.estado))
            conexion.commit()
            return True
        except Error as e:
            logger.error("Error al registrar proyecto: %s", e)
            return False
        finally:
            conexion.close()

    def listar_todos(self) -> list[Proyecto]:
        sql = "SELECT idProy, nomProy, fechaInicio, fechaFin, estado FROM proyecto"
        proyectos = []
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return proyectos
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                proyectos.append(Proyecto(
                    idProy=fila[0], nomProy=fila[1], fechaInicio=fila[2], fechaFin=fila[3], estado=fila[4]
                ))
            return proyectos
        except Error as e:
            logger.error("Error al listar proyectos: %s", e)
            return []
        finally:
            conexion.close()

    def actualizar(self, proy: Proyecto) -> bool:
        sql = "UPDATE proyecto SET nomProy = ?, fechaInicio = ?, fechaFin = ?, estado = ? WHERE idProy = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (proy.nomProy, proy.fechaInicio, proy.fechaFin, proy.estado, proy.idProy))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al actualizar proyecto: %s", e)
            return False
        finally:
            conexion.close()

    def eliminar(self, id_proy: int) -> bool:
        sql = "DELETE FROM proyecto WHERE idProy = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_proy,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al eliminar proyecto: %s", e)
            return False
        finally:
            conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (DAO PROYECTO) ---
# - registrar(proy): inserta nomProy, fechaInicio, fechaFin y estado usando marcadores (?).
# - listar_todos(): consulta todos los proyectos y los transforma en instancias Proyecto.
# - actualizar(proy): actualiza nombre, fechas y estado segun idProy.
# - eliminar(id_proy): borra el proyecto por idProy (por ON DELETE CASCADE en BD elimina sus asignaciones y registros de tiempo).
