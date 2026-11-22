import math
from utils.validaciones import validar_fecha_iso
from dao.dao_registrotiempo import DAORegistroTiempo
from modelo.registrotiempo import RegistroTiempo
from modelo.empleado import Empleado
from modelo.proyecto import Proyecto
from controlador.controlador_base import ControladorBase

class ControladorRegistroTiempo(ControladorBase):
    def __init__(self):
        super().__init__()
        self.__dao = DAORegistroTiempo()

    def registrar_tiempo(self, fecha, horas, id_emp, id_proy):
        try:
            self._exigir_gerente()
            fecha_ok, error = validar_fecha_iso(fecha, "fecha")
            if error:
                return False, error
            fecha_txt, _ = fecha_ok

            horas_num = float(horas)
            if not math.isfinite(horas_num) or horas_num <= 0:
                return False, "Las horas trabajadas deben ser mayores a cero."

            emp = Empleado(idEmpleado=int(id_emp), nomEmp="", apellidoEmp="", direccionEmp="", telefono="", correoEmp="", salario=0, fechaContrato="")
            proy = Proyecto(idProy=int(id_proy), nomProy="", fechaInicio="")

            reg = RegistroTiempo(idReg=None, fecha=fecha_txt, horasTrabajadas=horas_num, empleado=emp, proyecto=proy)
            exito = self.__dao.registrar(reg)
            if exito:
                return True, "Horas registradas correctamente."
            return False, "Error al guardar el registro de tiempo."
        except PermissionError as e:
            return False, str(e)
        except ValueError:
            return False, "Formato numérico inválido para horas o ID."

    def listar_registros(self):
        self._exigir_gerente()
        return self.__dao.listar_todos()

    def eliminar_registro(self, id_reg):
        self._exigir_gerente()
        exito = self.__dao.eliminar(int(id_reg))
        if exito:
            return True, "Registro de tiempo eliminado."
        return False, "No se encontró el registro."

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR REGISTRO DE TIEMPO) ---
# - registrar_tiempo(fecha, horas, id_emp, id_proy): exige _exigir_gerente(), valida fecha AAAA-MM-DD con validar_fecha_iso() (para impedir entradas como '2022'), valida que horas sea un numero finito > 0 con math.isfinite(), y guarda el registro mediante DAORegistroTiempo capturando PermissionError y ValueError.
# - listar_registros(), eliminar_registro(): exigen _exigir_gerente() y consultan o eliminan en DAORegistroTiempo.
