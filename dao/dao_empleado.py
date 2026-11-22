from conex.conn import ConexionBD
from modelo.empleado import Empleado
from modelo.departamento import Departamento
from modelo.usuario import Usuario
from utils.registro import logger
from utils.cifrado import cifrar, descifrar
from sqlite3 import Error

class DAOEmpleado:
    def __init__(self):
        self.__conexion_provider = ConexionBD()

    def __correo_duplicado(self, correo: str, cursor, excluir_id: int = None) -> bool:
        """Verifica unicidad del correo a nivel aplicación (el correo está cifrado en BD)."""
        cursor.execute("SELECT idEmpleado, correoEmp FROM empleado")
        for fila in cursor.fetchall():
            correo_bd = descifrar(fila[1])
            if correo_bd.lower() == correo.lower():
                if excluir_id is None or fila[0] != excluir_id:
                    return True
        return False

    def registrar(self, empleado: Empleado, usuario: Usuario = None) -> bool:
        """C - Create: Inserta un nuevo empleado en la BD con correo y salario cifrados."""
        sql = """
            INSERT INTO empleado (nomEmp, apellidoEmp, direccionEmp, telefono, correoEmp, salario, fechaContrato, idDep)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            if self.__correo_duplicado(empleado.correoEmp, cursor):
                logger.error("Error al registrar empleado en la BD: UNIQUE constraint failed: empleado.correoEmp")
                return False
            id_dep = empleado.departamento.idDep if empleado.departamento else None
            cursor.execute(sql, (
                empleado.nomEmp,
                empleado.apellidoEmp,
                cifrar(empleado.direccionEmp) if empleado.direccionEmp else "",
                cifrar(empleado.telefono) if empleado.telefono else "",
                cifrar(empleado.correoEmp),
                cifrar(str(empleado.salario)),
                empleado.fechaContrato,
                id_dep,
            ))
            if usuario is not None:
                id_empleado = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO usuario (nombreUsuario, clave, rol, idEmpleado) VALUES (?, ?, ?, ?)",
                    (
                        usuario.nombreUsuario,
                        Usuario.generar_hash_clave(usuario.clave),
                        usuario.rol,
                        id_empleado,
                    ),
                )
            conexion.commit()
            return True
        except Error as e:
            conexion.rollback()
            logger.error("Error al registrar empleado en la BD: %s", e)
            return False
        finally:
            conexion.close()

    def listar_todos(self) -> list[Empleado]:
        """R - Read: Consulta todos los empleados, descifrando correo y salario."""
        sql = """
            SELECT e.idEmpleado, e.nomEmp, e.apellidoEmp, e.direccionEmp, e.telefono,
                   e.correoEmp, e.salario, e.fechaContrato, d.idDep, d.nomDep
            FROM empleado e
            LEFT JOIN departamento d ON d.idDep = e.idDep
            ORDER BY e.idEmpleado
        """
        empleados = []
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            return empleados
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                try:
                    salario = float(descifrar(str(fila[6])))
                except (ValueError, TypeError):
                    salario = 0.0
                emp = Empleado(
                    idEmpleado=fila[0],
                    nomEmp=fila[1],
                    apellidoEmp=fila[2],
                    direccionEmp=descifrar(fila[3]),
                    telefono=descifrar(fila[4]),
                    correoEmp=descifrar(fila[5]),
                    salario=salario,
                    fechaContrato=fila[7],
                    departamento=Departamento(fila[8], fila[9]) if fila[8] is not None else None,
                )
                empleados.append(emp)
            return empleados
        except Error as e:
            logger.error("Error al consultar empleados: %s", e)
            return []
        finally:
            conexion.close()

    def actualizar(self, empleado: Empleado) -> bool:
        """U - Update: Actualiza la información de un empleado existente con datos cifrados."""
        sql = """
            UPDATE empleado
            SET nomEmp = ?, apellidoEmp = ?, direccionEmp = ?, telefono = ?,
                correoEmp = ?, salario = ?, fechaContrato = ?
            WHERE idEmpleado = ?
        """
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            if self.__correo_duplicado(empleado.correoEmp, cursor, excluir_id=empleado.idEmpleado):
                return False
            cursor.execute(sql, (
                empleado.nomEmp,
                empleado.apellidoEmp,
                cifrar(empleado.direccionEmp) if empleado.direccionEmp else "",
                cifrar(empleado.telefono) if empleado.telefono else "",
                cifrar(empleado.correoEmp),
                cifrar(str(empleado.salario)),
                empleado.fechaContrato,
                empleado.idEmpleado,
            ))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al actualizar empleado: %s", e)
            return False
        finally:
            conexion.close()

    def eliminar(self, id_empleado: int) -> bool:
        """D - Delete: Elimina un empleado por su ID."""
        sql = "DELETE FROM empleado WHERE idEmpleado = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al eliminar empleado: %s", e)
            return False
        finally:
            conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (DAO EMPLEADO) ---
# - correoEmp y salario se CIFRAN con Fernet (utils/cifrado.py) antes de guardar en SQLite
#   y se DESCIFRAN al leer, por lo que en el archivo .db aparecen como tokens ilegibles.
# - __correo_duplicado(): como Fernet usa IV aleatorio, el mismo correo cifrado dos veces
#   produce tokens distintos; la unicidad se valida a nivel aplicación descifrando cada fila.
# - descifrar() tiene fallback: si el valor no es un token válido (ej. dato antiguo en texto plano)
#   retorna el valor original para compatibilidad.
# - registrar / actualizar / eliminar: misma lógica de siempre, con cifrado añadido en correo y salario.

