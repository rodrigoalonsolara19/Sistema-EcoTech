from modelo.roles import ADMINISTRADOR, GERENTE, RRHH


class ControladorBase:
    def __init__(self):
        self.__usuario_actual = None

    def configurar_usuario(self, usuario):
        self.__usuario_actual = usuario

    def _exigir_gerente(self):
        if self.__usuario_actual is None or self.__usuario_actual.rol not in (ADMINISTRADOR, GERENTE):
            raise PermissionError("Esta operación requiere el rol Gerente o Administrador.")
        return self.__usuario_actual

    def _exigir_administrador(self):
        if self.__usuario_actual is None or self.__usuario_actual.rol != ADMINISTRADOR:
            raise PermissionError("Esta operación requiere el rol Administrador.")
        return self.__usuario_actual

    def _exigir_rrhh(self):
        if self.__usuario_actual is None or self.__usuario_actual.rol not in (ADMINISTRADOR, RRHH):
            raise PermissionError("Esta operación requiere el rol RRHH o Administrador.")
        return self.__usuario_actual

    def _usuario_actual(self):
        return self.__usuario_actual

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR BASE) ---
# Por que existe este archivo: implementa el control de acceso (autorizacion) en la capa logica.
# - configurar_usuario(usuario): almacena en __usuario_actual quien inicio sesion.
# - _usuario_actual(): devuelve el usuario autenticado o None.
# - _exigir_gerente(): verifica que el rol sea ADMINISTRADOR o GERENTE; lanza PermissionError.
# - _exigir_administrador(): restringe operaciones criticas solo al rol ADMINISTRADOR.
# - _exigir_rrhh(): restringe el panel de pagos/salarios al rol RRHH o ADMINISTRADOR.

