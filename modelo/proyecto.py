class Proyecto:
    def __init__(self, idProy, nomProy, fechaInicio, fechaFin=None, estado="Activo"):
        self.__idProy = idProy
        self.__nomProy = nomProy
        self.__fechaInicio = fechaInicio
        self.__fechaFin = fechaFin
        self.__estado = estado

    @property
    def idProy(self):
        return self.__idProy

    @idProy.setter
    def idProy(self, valor):
        self.__idProy = valor

    @property
    def nomProy(self):
        return self.__nomProy

    @nomProy.setter
    def nomProy(self, valor):
        self.__nomProy = valor

    @property
    def fechaInicio(self):
        return self.__fechaInicio

    @fechaInicio.setter
    def fechaInicio(self, valor):
        self.__fechaInicio = valor

    @property
    def fechaFin(self):
        return self.__fechaFin

    @fechaFin.setter
    def fechaFin(self, valor):
        self.__fechaFin = valor

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

# --- NOTAS GENERALES DEL ARCHIVO (MODELO PROYECTO) ---
# - Entidad POO que representa un proyecto (idProy, nomProy, fechaInicio, fechaFin opcional y estado Activo/Finalizado).
# - Sus atributos privados (__) se consultan y modifican mediante @property y @setter.
