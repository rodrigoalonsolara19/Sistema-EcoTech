from conex.conn import ConexionBD
from modelo.asignacionproyecto import AsignacionProyecto
from modelo.empleado import Empleado
from modelo.departamento import Departamento
from modelo.proyecto import Proyecto
from utils.registro import logger
from utils.cifrado import descifrar
from sqlite3 import Error

class DAOAsignacionProyecto:
    def __init__(self):
        self.__conexion_provider = ConexionBD()

    def registrar(self, asig: AsignacionProyecto) -> bool:
        sql = "INSERT INTO asignacionproyecto (fechaAsignacion, idEmpleado, idProy) VALUES (?, ?, ?)"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            id_emp = asig.empleado.idEmpleado if asig.empleado else None
            id_proy = asig.proyecto.idProy if asig.proyecto else None
            cursor.execute(sql, (asig.fechaAsignacion, id_emp, id_proy))
            conexion.commit()
            return True
        except Error as e:
            logger.error("Error al registrar asignación: %s", e)
            return False
        finally:
            conexion.close()

    def listar_todas(self) -> list[AsignacionProyecto]:
        sql = """
            SELECT a.idAsProy, a.fechaAsignacion,
                   e.idEmpleado, e.nomEmp, e.apellidoEmp, e.direccionEmp,
                   e.telefono, e.correoEmp, e.salario, e.fechaContrato,
                   p.idProy, p.nomProy, p.fechaInicio, p.fechaFin, p.estado,
                   d.idDep, d.nomDep
            FROM asignacionproyecto a
            JOIN empleado e ON e.idEmpleado = a.idEmpleado
            JOIN proyecto p ON p.idProy = a.idProy
            LEFT JOIN departamento d ON d.idDep = e.idDep
            ORDER BY a.idAsProy
        """
        asignaciones = []
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return asignaciones
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                try:
                    salario_emp = float(descifrar(str(fila[8])))
                except (ValueError, TypeError):
                    salario_emp = 0.0
                empleado = Empleado(
                    idEmpleado=fila[2], nomEmp=fila[3], apellidoEmp=fila[4],
                    direccionEmp=descifrar(fila[5]) if fila[5] else "",
                    telefono=descifrar(fila[6]) if fila[6] else "",
                    correoEmp=descifrar(fila[7]) if fila[7] else "",
                    salario=salario_emp, fechaContrato=fila[9],
                    departamento=Departamento(fila[15], fila[16]) if fila[15] is not None else None,
                )
                proyecto = Proyecto(
                    idProy=fila[10], nomProy=fila[11], fechaInicio=fila[12],
                    fechaFin=fila[13], estado=fila[14],
                )
                asignaciones.append(AsignacionProyecto(
                    idAsProy=fila[0], fechaAsignacion=fila[1],
                    empleado=empleado, proyecto=proyecto,
                ))
            return asignaciones
        except Error as e:
            logger.error("Error al consultar asignaciones: %s", e)
            return []
        finally:
            conexion.close()

    def eliminar(self, id_asig: int) -> bool:
        sql = "DELETE FROM asignacionproyecto WHERE idAsProy = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_asig,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al eliminar asignación: %s", e)
            return False
        finally:
            conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (DAO ASIGNACION DE PROYECTO) ---
# - registrar(asig): inserta fechaAsignacion, idEmpleado e idProy en asignacionproyecto usando SQL parametrizado (?).
# - listar_todas(): hace JOIN con empleado, proyecto y LEFT JOIN departamento para reconstruir AsignacionProyecto con sus objetos relacionados.
# - eliminar(id_asig): borra una asignacion por idAsProy y registra fallos SQLite en errores.log.
