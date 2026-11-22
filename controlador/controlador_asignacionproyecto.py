from dao.dao_asignacionproyecto import DAOAsignacionProyecto
from utils.validaciones import validar_fecha_iso
from modelo.asignacionproyecto import AsignacionProyecto
from modelo.empleado import Empleado
from modelo.proyecto import Proyecto
from controlador.controlador_base import ControladorBase

class ControladorAsignacionProyecto(ControladorBase):
    def __init__(self):
        super().__init__()
        self.__dao = DAOAsignacionProyecto()

    def registrar_asignacion(self, fecha_asig, id_emp, id_proy):
        try:
            self._exigir_gerente()
            fecha_ok, error = validar_fecha_iso(fecha_asig, "fecha de asignación")
            if error:
                return False, error
            fecha_txt, _ = fecha_ok
            
            emp = Empleado(idEmpleado=int(id_emp), nomEmp="", apellidoEmp="", direccionEmp="", telefono="", correoEmp="", salario=0, fechaContrato="")
            proy = Proyecto(idProy=int(id_proy), nomProy="", fechaInicio="")
            
            asig = AsignacionProyecto(idAsProy=None, fechaAsignacion=fecha_txt, empleado=emp, proyecto=proy)
            exito = self.__dao.registrar(asig)
            if exito:
                return True, "Empleado asignado al proyecto exitosamente."
            return False, "Error al registrar la asignación."
        except PermissionError as e:
            return False, str(e)
        except ValueError:
            return False, "Los ID de empleado y proyecto deben ser valores numéricos."

    def listar_asignaciones(self):
        self._exigir_gerente()
        return self.__dao.listar_todas()

    def eliminar_asignacion(self, id_asig):
        self._exigir_gerente()
        exito = self.__dao.eliminar(int(id_asig))
        if exito:
            return True, "Asignación eliminada correctamente."
        return False, "No se encontró la asignación."

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR ASIGNACION DE PROYECTO) ---
# - registrar_asignacion(fecha_asig, id_emp, id_proy): exige _exigir_gerente(), valida que la fecha cumpla formato real AAAA-MM-DD mediante validar_fecha_iso() (evitando textos invalidos) y convierte los IDs a entero antes de guardar en DAOAsignacionProyecto; captura PermissionError y ValueError.
# - listar_asignaciones(), eliminar_asignacion(): exigen _exigir_gerente() y delegan en DAOAsignacionProyecto.
