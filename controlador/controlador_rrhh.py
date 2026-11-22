from controlador.controlador_base import ControladorBase
from dao.dao_empleado import DAOEmpleado
from dao.dao_rrhh import DAORegistroPago
from servicio.servicio_indicadores import ServicioIndicadores, ErrorAPI


class ControladorRRHH(ControladorBase):
    """Controlador exclusivo del módulo de Recursos Humanos (pago de salarios)."""

    def __init__(self):
        super().__init__()
        self.__dao_emp = DAOEmpleado()
        self.__dao_pago = DAORegistroPago()
        self.__servicio = ServicioIndicadores()

    @property
    def fuente_usada(self):
        return self.__servicio.fuente_usada

    # ------------------------------------------------------------------ #
    # Helpers internos                                                     #
    # ------------------------------------------------------------------ #
    def __obtener_tipos_cambio(self):
        """Consulta UF, Dólar, Euro y UTM actuales. Devuelve (dict, error)."""
        tipos = {}
        try:
            for codigo in ("uf", "dolar", "euro", "utm"):
                serie = self.__servicio.ultimos_valores(codigo)["serie"]
                if not serie:
                    return None, f"No hay valor disponible para {codigo.upper()}."
                tipos[codigo] = serie[0]["valor"]
            return tipos, None
        except ErrorAPI as e:
            return None, f"No fue posible obtener los tipos de cambio: {e}"
        except Exception:
            return None, "Error inesperado al consultar los tipos de cambio."

    # ------------------------------------------------------------------ #
    # Métodos públicos                                                     #
    # ------------------------------------------------------------------ #
    def listar_empleados(self):
        """Lista todos los empleados (accesible para RRHH y Administrador)."""
        try:
            self._exigir_rrhh()
            return self.__dao_emp.listar_todos(), None
        except PermissionError as e:
            return [], str(e)

    def ver_salarios(self):
        """Devuelve nombre, correo y salario de todos los empleados."""
        try:
            self._exigir_rrhh()
            empleados = self.__dao_emp.listar_todos()
            resultado = []
            for e in empleados:
                resultado.append({
                    "id": e.idEmpleado,
                    "nombre": f"{e.nomEmp} {e.apellidoEmp}",
                    "correo": e.correoEmp,
                    "salario": e.salario,
                })
            return resultado, None
        except PermissionError as e:
            return [], str(e)

    def calcular_pago_empleado(self, id_empleado_texto):
        """Convierte el salario CLP de un empleado a UF/Dólar/Euro/UTM y lo persiste."""
        try:
            self._exigir_rrhh()
            try:
                id_emp = int(id_empleado_texto)
            except (ValueError, TypeError):
                return None, "El ID del empleado debe ser un número entero."
            # Buscar empleado
            empleados = self.__dao_emp.listar_todos()
            emp = next((e for e in empleados if e.idEmpleado == id_emp), None)
            if emp is None:
                return None, f"No se encontró un empleado con ID {id_emp}."
            salario = emp.salario
            # Obtener tipos de cambio
            tipos, error = self.__obtener_tipos_cambio()
            if error:
                return None, error
            conversiones = {
                "nombre": f"{emp.nomEmp} {emp.apellidoEmp}",
                "correo": emp.correoEmp,
                "salarioCLP": salario,
                "uf": {"valor": tipos["uf"], "equivale": salario / tipos["uf"]},
                "dolar": {"valor": tipos["dolar"], "equivale": salario / tipos["dolar"]},
                "euro": {"valor": tipos["euro"], "equivale": salario / tipos["euro"]},
                "utm": {"valor": tipos["utm"], "equivale": salario / tipos["utm"]},
            }
            # Persistir en BD
            self.__dao_pago.guardar_pago(
                id_empleado=id_emp,
                salario_clp=salario,
                valor_uf=tipos["uf"],
                valor_dolar=tipos["dolar"],
                valor_euro=tipos["euro"],
                valor_utm=tipos["utm"],
                fuente=self.__servicio.fuente_usada or "",
            )
            return conversiones, f"Pago calculado y guardado (fuente: {self.__servicio.fuente_usada})."
        except PermissionError as e:
            return None, str(e)
        except Exception:
            return None, "Error inesperado al calcular el pago."

    def listar_pagos(self):
        """Historial de pagos registrados."""
        try:
            self._exigir_rrhh()
            return self.__dao_pago.listar_pagos(), None
        except PermissionError as e:
            return [], str(e)

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR RRHH) ---
# - Solo acceden los roles RRHH y ADMINISTRADOR (_exigir_rrhh()).
# - ver_salarios(): expone nombre, correo y salario de cada empleado (datos sensibles controlados por rol).
# - calcular_pago_empleado(id): busca el empleado, consulta los 4 tipos de cambio actuales con
#   ServicioIndicadores y persiste el resultado en registropago via DAORegistroPago.
# - listar_pagos(): retorna el historial de pagos guardados en SQLite.
