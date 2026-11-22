from dao.dao_departamento import DAODepartamento
from modelo.departamento import Departamento
from controlador.controlador_base import ControladorBase

class ControladorDepartamento(ControladorBase):
    def __init__(self):
        super().__init__()
        self.__dao = DAODepartamento()

    def registrar_departamento(self, nom_dep):
        self._exigir_gerente()
        if not nom_dep.strip():
            return False, "El nombre del departamento no puede estar vacío."
        
        dep = Departamento(idDep=None, nomDep=nom_dep.strip())
        exito = self.__dao.registrar(dep)
        if exito:
            return True, "Departamento registrado exitosamente."
        return False, "Error al guardar el departamento."

    def listar_departamentos(self):
        self._exigir_gerente()
        return self.__dao.listar_todos()

    def actualizar_departamento(self, id_dep, nom_dep):
        self._exigir_gerente()
        if not nom_dep.strip():
            return False, "El nombre del departamento no puede estar vacío."
            
        dep = Departamento(idDep=int(id_dep), nomDep=nom_dep.strip())
        exito = self.__dao.actualizar(dep)
        if exito:
            return True, "Departamento actualizado correctamente."
        return False, "No se encontró el departamento."

    def eliminar_departamento(self, id_dep):
        self._exigir_gerente()
        exito = self.__dao.eliminar(int(id_dep))
        if exito:
            return True, "Departamento eliminado con éxito."
        return False, "No se encontró el departamento."

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR DEPARTAMENTO) ---
# - registrar_departamento(nom_dep): exige _exigir_gerente(), valida que el nombre no este vacio tras .strip() y lo guarda via DAODepartamento.
# - listar_departamentos(): exige _exigir_gerente() y retorna la lista de objetos Departamento desde SQLite.
# - actualizar_departamento(id_dep, nom_dep): exige _exigir_gerente(), valida nombre no vacio y actualiza por idDep.
# - eliminar_departamento(id_dep): exige _exigir_gerente() y elimina por idDep (los empleados asociados pasan a idDep = NULL por ON DELETE SET NULL).
