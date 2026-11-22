import math

class Empleado:
    def __init__(self, idEmpleado, nomEmp, apellidoEmp, direccionEmp, telefono, correoEmp, salario, fechaContrato, departamento=None):
        self.__idEmpleado = idEmpleado
        self.__nomEmp = nomEmp
        self.__apellidoEmp = apellidoEmp
        self.__direccionEmp = direccionEmp
        self.__telefono = telefono
        self.__correoEmp = correoEmp
        self.salario = salario
        self.__fechaContrato = fechaContrato
        self.__departamento = departamento

    @property
    def idEmpleado(self):
        return self.__idEmpleado

    @idEmpleado.setter
    def idEmpleado(self, valor):
        self.__idEmpleado = valor

    @property
    def nomEmp(self):
        return self.__nomEmp

    @nomEmp.setter
    def nomEmp(self, valor):
        self.__nomEmp = valor

    @property
    def apellidoEmp(self):
        return self.__apellidoEmp

    @apellidoEmp.setter
    def apellidoEmp(self, valor):
        self.__apellidoEmp = valor

    @property
    def direccionEmp(self):
        return self.__direccionEmp

    @direccionEmp.setter
    def direccionEmp(self, valor):
        self.__direccionEmp = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor

    @property
    def correoEmp(self):
        return self.__correoEmp

    @correoEmp.setter
    def correoEmp(self, valor):
        self.__correoEmp = valor

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, valor):
        val_num = float(valor)
        if math.isfinite(val_num) and val_num >= 0:
            self.__salario = val_num
        else:
            raise ValueError("El salario debe ser un número finito no negativo.")

    @property
    def fechaContrato(self):
        return self.__fechaContrato

    @fechaContrato.setter
    def fechaContrato(self, valor):
        self.__fechaContrato = valor

    @property
    def departamento(self):
        return self.__departamento

    @departamento.setter
    def departamento(self, valor):
        self.__departamento = valor

# --- NOTAS GENERALES DEL ARCHIVO (MODELO EMPLEADO) ---
# - Entidad POO que representa a un empleado (datos personales, salario, fechaContrato y objeto departamento asociado).
# - Protege sus atributos con encapsulamiento (__) y en el setter de salario exige un numero finito (math.isfinite) mayor o igual a cero.
