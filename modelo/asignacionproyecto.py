class AsignacionProyecto:
    def __init__(self, idAsProy, fechaAsignacion, empleado=None, proyecto=None):
        self.__idAsProy = idAsProy
        self.__fechaAsignacion = fechaAsignacion
        self.__empleado = empleado
        self.__proyecto = proyecto

    @property
    def idAsProy(self):
        return self.__idAsProy

    @idAsProy.setter
    def idAsProy(self, valor):
        self.__idAsProy = valor

    @property
    def fechaAsignacion(self):
        return self.__fechaAsignacion

    @fechaAsignacion.setter
    def fechaAsignacion(self, valor):
        self.__fechaAsignacion = valor

    @property
    def empleado(self):
        return self.__empleado

    @empleado.setter
    def empleado(self, valor):
        self.__empleado = valor

    @property
    def proyecto(self):
        return self.__proyecto

    @proyecto.setter
    def proyecto(self, valor):
        self.__proyecto = valor

# --- NOTAS GENERALES DEL ARCHIVO (MODELO ASIGNACION DE PROYECTO) ---
# - Entidad POO que vincula un Empleado con un Proyecto en una fechaAsignacion determinada.
# - Usa encapsulamiento (__) con @property y @setter para todos sus atributos.
