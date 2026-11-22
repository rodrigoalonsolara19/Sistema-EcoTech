class Departamento:
    def __init__(self, idDep, nomDep, gerente=None, empleados=None):
        self.__idDep = idDep
        self.__nomDep = nomDep
        self.__gerente = gerente
        self.__empleados = empleados if empleados is not None else []

    @property
    def idDep(self):
        return self.__idDep

    @idDep.setter
    def idDep(self, valor):
        self.__idDep = valor

    @property
    def nomDep(self):
        return self.__nomDep

    @nomDep.setter
    def nomDep(self, valor):
        self.__nomDep = valor

    @property
    def gerente(self):
        return self.__gerente

    @gerente.setter
    def gerente(self, valor):
        self.__gerente = valor

    @property
    def empleados(self):
        return self.__empleados

    @empleados.setter
    def empleados(self, valor):
        self.__empleados = valor

# --- NOTAS GENERALES DEL ARCHIVO (MODELO DEPARTAMENTO) ---
# - Entidad POO que representa un departamento de la empresa (idDep, nomDep, gerente y lista de empleados).
# - Usa atributos privados (__) expuestos mediante @property y @setter para mantener encapsulamiento.
