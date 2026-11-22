import math

class RegistroTiempo:
    def __init__(self, idReg, fecha, horasTrabajadas, empleado=None, proyecto=None):
        self.__idReg = idReg
        self.__fecha = fecha
        self.horasTrabajadas = horasTrabajadas
        self.__empleado = empleado
        self.__proyecto = proyecto

    @property
    def idReg(self):
        return self.__idReg

    @idReg.setter
    def idReg(self, valor):
        self.__idReg = valor

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, valor):
        self.__fecha = valor

    @property
    def horasTrabajadas(self):
        return self.__horasTrabajadas

    @horasTrabajadas.setter
    def horasTrabajadas(self, valor):
        valor = float(valor)
        if math.isfinite(valor) and valor > 0:
            self.__horasTrabajadas = valor
        else:
            raise ValueError("Las horas trabajadas deben ser un número finito mayor a 0.")

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

# --- NOTAS GENERALES DEL ARCHIVO (MODELO REGISTRO DE TIEMPO) ---
# - Entidad POO que registra las horasTrabajadas por un empleado en un proyecto en una fecha dada.
# - El setter de horasTrabajadas valida con math.isfinite() que las horas sean un numero finito mayor a 0.
