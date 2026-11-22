from conex.conn import ConexionBD
from modelo.registrotiempo import RegistroTiempo
from modelo.empleado import Empleado
from modelo.departamento import Departamento
from modelo.proyecto import Proyecto
from utils.registro import logger
from utils.cifrado import descifrar
from sqlite3 import Error

class DAORegistroTiempo:
    def __init__(self):
        self.__conexion_provider = ConexionBD()

    def registrar(self, reg: RegistroTiempo) -> bool:
        sql = "INSERT INTO registrotiempo (fecha, horasTrabajadas, idEmpleado, idProy) VALUES (?, ?, ?, ?)"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            id_emp = reg.empleado.idEmpleado if reg.empleado else None
            id_proy = reg.proyecto.idProy if reg.proyecto else None
            cursor.execute(sql, (reg.fecha, reg.horasTrabajadas, id_emp, id_proy))
            conexion.commit()
            return True
        except Error as e:
            logger.error("Error al registrar tiempo: %s", e)
            return False
        finally:
            conexion.close()

    def listar_todos(self) -> list[RegistroTiempo]:
        sql = """
            SELECT r.idReg, r.fecha, r.horasTrabajadas,
                   e.idEmpleado, e.nomEmp, e.apellidoEmp, e.direccionEmp,
                   e.telefono, e.correoEmp, e.salario, e.fechaContrato,
                   p.idProy, p.nomProy, p.fechaInicio, p.fechaFin, p.estado,
                   d.idDep, d.nomDep
            FROM registrotiempo r
            JOIN empleado e ON e.idEmpleado = r.idEmpleado
            JOIN proyecto p ON p.idProy = r.idProy
            LEFT JOIN departamento d ON d.idDep = e.idDep
            ORDER BY r.idReg
        """
        registros = []
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return registros
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                try:
                    salario_emp = float(descifrar(str(fila[9])))
                except (ValueError, TypeError):
                    salario_emp = 0.0
                empleado = Empleado(
                    idEmpleado=fila[3], nomEmp=fila[4], apellidoEmp=fila[5],
                    direccionEmp=descifrar(fila[6]) if fila[6] else "",
                    telefono=descifrar(fila[7]) if fila[7] else "",
                    correoEmp=descifrar(fila[8]) if fila[8] else "",
                    salario=salario_emp, fechaContrato=fila[10],
                    departamento=Departamento(fila[16], fila[17]) if fila[16] is not None else None,
                )
                proyecto = Proyecto(
                    idProy=fila[11], nomProy=fila[12], fechaInicio=fila[13],
                    fechaFin=fila[14], estado=fila[15],
                )
                registros.append(RegistroTiempo(
                    idReg=fila[0], fecha=fila[1], horasTrabajadas=fila[2],
                    empleado=empleado, proyecto=proyecto,
                ))
            return registros
        except Error as e:
            logger.error("Error al consultar registros de tiempo: %s", e)
            return []
        finally:
            conexion.close()

    def eliminar(self, id_reg: int) -> bool:
        sql = "DELETE FROM registrotiempo WHERE idReg = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_reg,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al eliminar registro de tiempo: %s", e)
            return False
        finally:
            conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (DAO REGISTRO DE TIEMPO) ---
# - registrar(reg): guarda fecha, horasTrabajadas, idEmpleado e idProy usando marcadores (?) contra Inyeccion SQL.
# - listar_todos(): une registrotiempo con empleado, proyecto y departamento mediante JOIN para devolver objetos RegistroTiempo completos.
# - eliminar(id_reg): elimina un registro de horas por idReg y registra posibles errores SQLite en errores.log.
