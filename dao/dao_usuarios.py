import hmac
from conex.conn import ConexionBD
from modelo.usuario import Usuario
from modelo.empleado import Empleado
from modelo.departamento import Departamento
from modelo.roles import ADMINISTRADOR
from utils.registro import logger
from utils.cifrado import descifrar
from sqlite3 import Error

class DAOUsuarios:
    def __init__(self):
        self.__conexion_provider = ConexionBD()

    def hay_administradores(self) -> bool:
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            raise RuntimeError("No se pudo conectar a la base de datos para verificar administradores.")
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT 1 FROM usuario WHERE UPPER(TRIM(rol)) IN (?, ?) LIMIT 1",
                (ADMINISTRADOR, "ADMIN"),
            )
            return cursor.fetchone() is not None
        except Error as e:
            raise RuntimeError(f"No se pudo verificar si existen administradores: {e}") from e
        finally:
            conexion.close()


    def registrar_administrador_inicial(self, usuario: Usuario) -> bool:
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            raise RuntimeError("No se pudo conectar a la base de datos para crear el administrador.")
        try:
            conexion.execute("BEGIN IMMEDIATE")
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT 1 FROM usuario WHERE UPPER(TRIM(rol)) IN (?, ?) LIMIT 1",
                (ADMINISTRADOR, "ADMIN"),
            )
            if cursor.fetchone() is not None:
                return False
            cursor.execute(
                "INSERT INTO usuario (nombreUsuario, clave, rol, idEmpleado) VALUES (?, ?, ?, NULL)",
                (usuario.nombreUsuario, Usuario.generar_hash_clave(usuario.clave), ADMINISTRADOR),
            )
            conexion.commit()
            return True
        except Error as e:
            conexion.rollback()
            raise RuntimeError(f"No se pudo crear el administrador: {e}") from e
        finally:
            conexion.close()


    def registrar(self, usuario: Usuario) -> bool:
        sql = "INSERT INTO usuario (nombreUsuario, clave, rol, idEmpleado) VALUES (?, ?, ?, ?)"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            id_emp = usuario.empleado.idEmpleado if usuario.empleado else None
            cursor.execute(sql, (
                usuario.nombreUsuario,
                Usuario.generar_hash_clave(usuario.clave),
                usuario.rol,
                id_emp,
            ))
            conexion.commit()
            return True
        except Error as e:
            logger.error("Error al registrar usuario: %s", e)
            return False
        finally:
            conexion.close()


    def autenticar(self, nombre_usuario: str, clave: str):
        sql = """
            SELECT u.nombreUsuario, u.clave, u.rol, e.idEmpleado, e.nomEmp,
                   e.apellidoEmp, e.direccionEmp, e.telefono, e.correoEmp,
                   e.salario, e.fechaContrato, d.idDep, d.nomDep
            FROM usuario u
            LEFT JOIN empleado e ON e.idEmpleado = u.idEmpleado
            LEFT JOIN departamento d ON d.idDep = e.idDep
            WHERE u.nombreUsuario = ?
        """
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            raise RuntimeError("No se pudo conectar a la base de datos para iniciar sesión.")
            
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (nombre_usuario,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            if not Usuario.verificar_clave(clave, fila[1]):
                if not hmac.compare_digest(clave.encode("utf-8"), fila[1].encode("utf-8")):
                    return None
                cursor.execute(
                    "UPDATE usuario SET clave = ? WHERE nombreUsuario = ?",
                    (Usuario.generar_hash_clave(clave), nombre_usuario),
                )
                conexion.commit()
            elif not fila[1].startswith(("$2a$", "$2b$", "$2y$")):
                cursor.execute(
                    "UPDATE usuario SET clave = ? WHERE nombreUsuario = ?",
                    (Usuario.generar_hash_clave(clave), nombre_usuario),
                )
                conexion.commit()
            empleado = None
            if fila[3] is not None:
                try:
                    salario_emp = float(descifrar(str(fila[9])))
                except (ValueError, TypeError):
                    salario_emp = 0.0
                empleado = Empleado(
                    idEmpleado=fila[3],
                    nomEmp=fila[4],
                    apellidoEmp=fila[5],
                    direccionEmp=descifrar(fila[6]) if fila[6] else "",
                    telefono=descifrar(fila[7]) if fila[7] else "",
                    correoEmp=descifrar(fila[8]) if fila[8] else "",
                    salario=salario_emp,
                    fechaContrato=fila[10],
                    departamento=Departamento(fila[11], fila[12]) if fila[11] is not None else None,
                )
            return Usuario(clave="", rol=fila[2], nombreUsuario=fila[0], empleado=empleado)
        except Error as e:
            raise RuntimeError(f"No se pudo validar el inicio de sesión: {e}") from e
        finally:
            conexion.close()


    def listar_todos(self) -> list[Usuario]:
        sql = """
            SELECT u.nombreUsuario, u.rol, e.idEmpleado, e.nomEmp, e.apellidoEmp,
                   e.direccionEmp, e.telefono, e.correoEmp, e.salario, e.fechaContrato,
                   d.idDep, d.nomDep
            FROM usuario u
            LEFT JOIN empleado e ON e.idEmpleado = u.idEmpleado
            LEFT JOIN departamento d ON d.idDep = e.idDep
            ORDER BY u.nombreUsuario
        """
        usuarios = []
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return usuarios
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            for fila in filas:
                empleado = None
                if fila[2] is not None:
                    try:
                        salario_emp = float(descifrar(str(fila[8])))
                    except (ValueError, TypeError):
                        salario_emp = 0.0
                    empleado = Empleado(
                        idEmpleado=fila[2],
                        nomEmp=fila[3],
                        apellidoEmp=fila[4],
                        direccionEmp=descifrar(fila[5]) if fila[5] else "",
                        telefono=descifrar(fila[6]) if fila[6] else "",
                        correoEmp=descifrar(fila[7]) if fila[7] else "",
                        salario=salario_emp,
                        fechaContrato=fila[9],
                        departamento=Departamento(fila[10], fila[11]) if fila[10] is not None else None,
                    )
                try:
                    usuarios.append(Usuario(clave="", rol=fila[1], nombreUsuario=fila[0], empleado=empleado))
                except ValueError as e:
                    logger.warning("Usuario '%s' omitido por el rol inválido (%s): %s", fila[0], fila[1        ], e)
            return usuarios
        except Error as e:
            logger.error("Error al consultar usuarios: %s", e)
            return []
        finally:
            conexion.close()


    def eliminar(self, nombre_usuario: str) -> bool:
        sql = "DELETE FROM usuario WHERE nombreUsuario = ?"
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion: return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (nombre_usuario,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error("Error al eliminar usuario: %s", e)
            return False
        finally:
            conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (DAO USUARIOS) ---
# Por que existe este archivo: encapsula todas las consultas SQL de la tabla usuario usando marcadores parametrizados (?) para impedir Inyeccion SQL.
# - hay_administradores(): verifica con SELECT 1 ... LIMIT 1 si ya existe algun Administrador en la BD.
# - registrar_administrador_inicial(usuario): usa BEGIN IMMEDIATE para crear de forma atomica al primer Administrador (hasheado con bcrypt) solo si no existe otro.
# - registrar(usuario): inserta usuario, clave hasheada con Usuario.generar_hash_clave() (bcrypt), rol y posible idEmpleado.
# - autenticar(nombre_usuario, clave): consulta usuario + empleado + departamento (LEFT JOIN); valida clave con Usuario.verificar_clave() (bcrypt) y, si la cuenta antigua tenia texto plano o pbkdf2_sha256$, actualiza automaticamente el registro a bcrypt en la BD.
# - listar_todos(): recorre filas reconstruyendo cada Usuario y su Empleado. El try/except ValueError va DENTRO del for para omitir y registrar en errores.log (logger.warning) solo un registro con rol invalido sin detener el listado completo; except Error queda fuera para fallos SQL retornando [].
# - eliminar(nombre_usuario): borra la cuenta por nombreUsuario y retorna True si rowcount > 0.

