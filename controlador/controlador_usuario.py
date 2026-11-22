from utils.validaciones import patronUsuario, validar_clave
from controlador.controlador_base import ControladorBase
from dao.dao_usuarios import DAOUsuarios
from modelo.empleado import Empleado
from modelo.roles import ADMINISTRADOR, normalizar_rol
from modelo.usuario import Usuario
import re


class ControladorUsuario(ControladorBase):
    def __init__(self):
        super().__init__()
        self.__dao = DAOUsuarios()

    def hay_administradores(self):
        return self.__dao.hay_administradores()

    def registrar_administrador_inicial(self, nombre_usuario, clave):
        nombre_usuario = nombre_usuario.strip()
        if not re.fullmatch(patronUsuario, nombre_usuario):
            return False, f"El usuario debe tener de 4 a 20 caracteres (letras, números, _ . -)."
        error_clave = validar_clave(clave)
        if error_clave:
            return False, error_clave
        usuario = Usuario(clave=clave, rol = ADMINISTRADOR, nombreUsuario=nombre_usuario)
        try:
            if self.__dao.registrar_administrador_inicial(usuario):
                return True, "Administrador inicial creado. Inicie sesión."
            return False, "Ya existe un Administrador; no se puede volver a crear."
        except RuntimeError as e:
            return False, str(e)

    def iniciar_sesion(self, nombre_usuario, clave):
        if not nombre_usuario.strip() or not clave:
            return None, "Ingrese usuario y contraseña."
        try:
            usuario = self.__dao.autenticar(nombre_usuario.strip(), clave)
        except ValueError as e:
            raise RuntimeError(f"La cuenta tiene un rol inválido; corrija el rol antes de iniciar sesión: {e}") from e
        if usuario is None:
            return None, "Usuario o contraseña incorrectos."
        return usuario, "Inicio de sesión correcto."

    def registrar_usuario(self, nombre_usuario, clave, rol, id_empleado=None):
        nombre_usuario = nombre_usuario.strip()
        if not re.fullmatch(patronUsuario, nombre_usuario):
            return False, "El usuario debe tener de 4 a 20 caracteres (letras, números, _ . -)."
        error_clave = validar_clave(clave)
        if error_clave:
            return False, error_clave
        try:
            actor = self._exigir_gerente()
            rol = normalizar_rol(rol)
            if rol == ADMINISTRADOR and actor.rol != ADMINISTRADOR:
                return False, "Solo un Administrador puede crear cuentas Administrador."
            if rol == ADMINISTRADOR and id_empleado is not None:
                return False, "Las cuentas Administrador no se asocian a un empleado."
            emp_obj = None
            if id_empleado is not None:
                emp_obj = Empleado(
                    idEmpleado=int(id_empleado),
                    nomEmp="",
                    apellidoEmp="",
                    direccionEmp="",
                    telefono="",
                    correoEmp="",
                    salario=0,
                    fechaContrato="",
                )
            usuario = Usuario(clave=clave, rol=rol, nombreUsuario=nombre_usuario, empleado=emp_obj)
            if self.__dao.registrar(usuario):
                return True, "Usuario registrado exitosamente."
            return False, "No se pudo registrar el usuario; verifique duplicados y empleado asociado."
        except PermissionError as e:
            return False, str(e)
        except ValueError:
            return False, "El rol o el ID de empleado no es válido."

    def listar_usuarios(self):
        actor = self._exigir_gerente()
        usuarios = self.__dao.listar_todos()
        if actor.rol == ADMINISTRADOR:
            return usuarios
        return [usuario for usuario in usuarios if usuario.rol != ADMINISTRADOR]

    def eliminar_usuario(self, nombre_usuario):
        try:
            actor = self._exigir_gerente()
            if actor.nombreUsuario == nombre_usuario:
                return False, "No puede eliminar la cuenta con la que inició sesión."
            usuarios = self.__dao.listar_todos()
            encontrado = next((u for u in usuarios if u.nombreUsuario == nombre_usuario), None)
            if encontrado is None:
                return False, "No se encontró el usuario."
            if encontrado.rol == ADMINISTRADOR and actor.rol != ADMINISTRADOR:
                return False, "Solo un Administrador puede eliminar cuentas Administrador."
            if encontrado.rol == ADMINISTRADOR and sum(u.rol == ADMINISTRADOR for u in usuarios) <= 1:
                return False, "Debe quedar al menos un Administrador en el sistema."
            if self.__dao.eliminar(nombre_usuario):
                return True, "Usuario eliminado correctamente."
            return False, "No se encontró el usuario."
        except PermissionError as e:
            return False, str(e)

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR USUARIOS) ---
# - hay_administradores(): delega al DAO para saber si el sistema requiere configuracion inicial de Administrador.
# - registrar_administrador_inicial(nombre_usuario, clave): valida patronUsuario tras .strip() y clave con validar_clave() (14 chars min, 72 bytes max), y crea el primer Admin en transaccion segura.
# - iniciar_sesion(nombre_usuario, clave): valida campos no vacios, llama a DAOUsuarios.autenticar() y convierte ValueError (rol invalido en BD) en RuntimeError controlada.
# - registrar_usuario(nombre_usuario, clave, rol, id_empleado): valida formato de usuario y clave, exige _exigir_gerente(), normaliza rol y prohibe que un Gerente cree cuentas Administrador o asocie un empleado a una cuenta Administrador.
# - listar_usuarios(): exige Gerente/Admin y oculta cuentas ADMINISTRADOR si quien consulta es Gerente.
# - eliminar_usuario(nombre_usuario): impide auto-eliminarse, impide que un Gerente borre a un Admin y bloquea eliminar al ultimo Administrador del sistema.

