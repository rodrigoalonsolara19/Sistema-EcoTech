from conex.conn import ConexionBD
from modelo.departamento import Departamento
from utils.registro import logger
from sqlite3 import Error

class DAODepartamento:
    def __init__(self):
        self.__conexion_provider = ConexionBD()

    def registrar(self, dep: Departamento) -> bool:
        sql = "INSERT INTO departamento (nomDep) VALUES (?)"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (dep.nomDep,))
            conexion.commit()
            return True
        except Error as e:
            logger.error("Error al registrar departamento: %s", e)
            return False
        finally:
            conexion.close()

    def listar_todos(self) -> list[Departamento]:
        sql = "SELECT idDep, nomDep FROM departamento"
        departamentos = []
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return departamentos
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                departamentos.append(Departamento(idDep=fila[0], nomDep=fila[1]))
            return departamentos
        except Error as e:
            logger.error("Error al consultar departamentos: $s", e)
            return []
        finally:
            conexion.close()

    def actualizar(self, dep: Departamento) -> bool:
        sql = "UPDATE departamento SET nomDep = ? WHERE idDep = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (dep.nomDep, dep.idDep))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al actualizar departamento: %s", e)
            return False
        finally:
            conexion.close()

    def eliminar(self, id_dep: int) -> bool:
        sql = "DELETE FROM departamento WHERE idDep = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_dep,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al eliminar departamento: %s", e)
            return False
        finally:
            conexion.close()

    def existe(self, id_dep: int) -> bool:
        """Verifica si un departamento existe por su ID"""
        sql = "SELECT 1 FROM departamento WHERE idDep = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_dep,))
            return cursor.fetchone() is not None
        except Error:
            return False
        finally:
            conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (DAO DEPARTAMENTO) ---
# - registrar(dep): inserta nomDep en tabla departamento usando parametro (?) contra Inyeccion SQL.
# - listar_todos(): lee todos los departamentos y retorna objetos Departamento.
# - actualizar(dep): modifica nomDep filtrando por idDep y retorna True si rowcount > 0.
# - eliminar(id_dep): elimina por idDep (por ON DELETE SET NULL, los empleados quedan con idDep = NULL).
# - existe(id_dep): consulta rapida SELECT 1 para que ControladorEmpleado valide si el departamento existe antes de registrar un empleado.
