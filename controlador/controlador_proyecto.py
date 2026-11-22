import re
from datetime import datetime
from dao.dao_proyecto import DAOProyecto
from modelo.proyecto import Proyecto
from controlador.controlador_base import ControladorBase

class ControladorProyecto(ControladorBase):
    def __init__(self):
        super().__init__()
        self.__dao = DAOProyecto()

    def __validar_datos(self, nom_proy, fecha_inicio, fecha_fin, estado):
        nom_limpio = nom_proy.strip()
        inicio_txt = fecha_inicio.strip()
        fin_txt = fecha_fin.strip() if fecha_fin else None
        estado_norm = (estado or "Activo").strip().capitalize()
        if not nom_limpio or not inicio_txt:
            return None, "El nombre y la fecha de inicio son obligatorios."
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", inicio_txt):
            return None, "La fecha de inicio debe tener formato AAAA-MM-DD."
        try:
            inicio_dt = datetime.strptime(inicio_txt, "%Y-%m-%d").date()
        except ValueError:
            return None, "La fecha de inicio no es una fecha válida."
        if fin_txt is not None:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fin_txt):
                return None, "La fecha de fin debe tener formato AAAA-MM-DD."
            try:
                fin_dt = datetime.strptime(fin_txt, "%Y-%m-%d").date()
            except ValueError:
                return None, "La fecha de fin no es una fecha válida."
            if fin_dt < inicio_dt:
                return None, "La fecha de fin no puede ser anterior a la fecha de inicio."
        if estado_norm not in ("Activo", "Finalizado"):
            return None, "El estado debe ser Activo o Finalizado."
        return (nom_limpio, inicio_txt, fin_txt, estado_norm), None

    def registrar_proyecto(self, nom_proy, fecha_inicio, fecha_fin=None, estado="Activo"):
        try:
            self._exigir_gerente()
            datos, error = self.__validar_datos(nom_proy, fecha_inicio, fecha_fin, estado)
            if error:
                return False, error
            nom_limpio, inicio_txt, fin_txt, estado_norm = datos
            proy = Proyecto(
                idProy=None,
                nomProy=nom_limpio,
                fechaInicio=inicio_txt,
                fechaFin=fin_txt,
                estado=estado_norm,
            )
            if self.__dao.registrar(proy):
                return True, "Proyecto creado correctamente.."
            return False, "Error al registrar el proyecto."
        except PermissionError as e:
            return False, str(e)

    def listar_proyectos(self):
        self._exigir_gerente()
        return self.__dao.listar_todos()

    def actualizar_proyecto(self, id_proy, nom_proy, fecha_inicio, fecha_fin, estado):
        try:
            self._exigir_gerente()
            datos, error = self.__validar_datos(nom_proy, fecha_inicio, fecha_fin, estado)
            if error:
                return False, error
            nom_limpio, inicio_txt, fin_txt, estado_norm = datos
            proy = Proyecto(
                idProy=int(id_proy),
                nomProy=nom_limpio,
                fechaInicio=inicio_txt,
                fechaFin=fin_txt,
                estado=estado_norm,
            )
            if self.__dao.actualizar(proy):
                return True, "Proyecto actualizado correctamente..."
            return False, "No se encontró el proyecto a actualizar."
        except PermissionError as e:
            return False, str(e)
        except ValueError:
            return False, "El ID del proyecto debe ser numérico.."

    def eliminar_proyecto(self, id_proy):
        self._exigir_gerente()
        exito = self.__dao.eliminar(int(id_proy))
        if exito:
            return True, "Proyecto eliminado correctamente."
        return False, "No se encontró el proyecto."

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR PROYECTO) ---
# - __validar_datos(nom_proy, fecha_inicio, fecha_fin, estado): se agrego para validar en un solo lugar las reglas de Proyecto antes de guardar o actualizar: nombre y fechaInicio obligatorios, formato exacto AAAA-MM-DD (regex + strptime), fechaFin >= fechaInicio si se entrega fecha de termino, y estado normalizado solo como Activo o Finalizado.
# - registrar_proyecto(), actualizar_proyecto(): exigen _exigir_gerente(), llaman a __validar_datos(), construyen Proyecto y capturan PermissionError/ValueError sin caidas.
# - listar_proyectos(), eliminar_proyecto(): exigen _exigir_gerente() y delegan en DAOProyecto.
