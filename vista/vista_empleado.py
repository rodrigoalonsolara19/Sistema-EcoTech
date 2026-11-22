from getpass import getpass
from controlador.controlador_empleado import ControladorEmpleado
from utils.validaciones import (
    validar_clave,
    validar_correo,
    validar_fecha_iso,
    validar_nombre,
    validar_salario,
    validar_telefono,
    validar_usuario,
)

class VistaEmpleado:
    def __init__(self):
        self.__controlador = ControladorEmpleado()

    def configurar_usuario(self, usuario):
        self.__controlador.configurar_usuario(usuario)

    def __pedir_valido(self, mensaje, validador, ocultar=False):
        while True:
            valor = getpass(mensaje) if ocultar else input(mensaje).strip()
            error = validador(valor)
            if error is None:
                return valor
            print(f"Incorrecto: {error}")
    def __pedir_opcional_entero(self, mensaje):
        while True:
            texto = input(mensaje).strip()
            if not texto:
                return None
            try:
                return int(texto)
            except ValueError:
                print("Incorrecto: El ID debe ser un número entero.")

    def menu(self):
        while True:
            print("\n--- GESTIÓN DE EMPLEADOS ---")
            print("1. Registrar Empleado")
            print("2. Listar Empleados")
            print("3. Actualizar Empleado")
            print("4. Eliminar Empleado")
            print("5. Volver al Menú Principal")
            
            opcion = input("Seleccione una opción (1-5): ").strip()

            if opcion == "1":
                self.__registrar()
            elif opcion == "2":
                self.__listar()
            elif opcion == "3":
                self.__actualizar()
            elif opcion == "4":
                self.__eliminar()
            elif opcion == "5":
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def __registrar(self):
        print("\n[ Registrar Empleado ]")
        nom = self.__pedir_valido("Nombre: ", lambda v: validar_nombre(v, "nombre"))
        ape = self.__pedir_valido("Apellido: ", lambda v: validar_nombre(v, "apellido"))
        dir_emp = input("Dirección: ").strip()
        tel = self.__pedir_valido("Teléfono: ", validar_telefono)
        correo = self.__pedir_valido("Correo electrónico: ", validar_correo)
        salario = self.__pedir_valido("Salario: ", validar_salario)
        f_contrato = self.__pedir_valido(
            "Fecha de Contrato (AAAA-MM-DD): ",
            lambda v: validar_fecha_iso(v, "fecha de contrato")[1],
        )
        id_dep = self.__pedir_opcional_entero("ID de Departamento (opcional, Presione Enter para omitir): ")
        nombre_usuario = self.__pedir_valido("Usuario de acceso: ", validar_usuario)
        clave = self.__pedir_valido("Contraseña (mínimo 14 caracteres): ", validar_clave, ocultar=True)
        roles = {"1": "EMPLEADO", "2": "GERENTE"}
        while True:
            print("Rol para la cuenta: 1. Empleado  2. Gerente")
            rol_opcion = input("Seleccione el rol: ").strip()
            if rol_opcion in roles:
                break
            print("Incorrecto: Rol no válido.")
        exito, msg = self.__controlador.registrar_empleado(
            nom, ape, dir_emp, tel, correo, salario, f_contrato, id_dep,
            nombre_usuario, clave, roles[rol_opcion]
        )
        print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")

    def __listar(self):
        print("\n[ Lista de Empleados ]")
        empleados = self.__controlador.listar_empleados()
        if not empleados:
            print("No existen empleados registrados.")
        else:
            for e in empleados:
                print(f"ID: {e.idEmpleado} | Nombre: {e.nomEmp} {e.apellidoEmp} | Correo: {e.correoEmp} | Salario: ${e.salario:,.2f}")

    def __actualizar(self):
        print("\n[ Actualizar Empleado ]")
        try:
            id_emp = int(input("ID del empleado a modificar: "))
            nom = input("Nuevo Nombre: ").strip()
            ape = input("Nuevo Apellido: ").strip()
            dir_emp = input("Nueva Dirección: ").strip()
            tel = input("Nuevo Teléfono: ").strip()
            correo = input("Nuevo Correo: ").strip()
            salario = input("Nuevo Salario: ").strip()
            f_contrato = input("Nueva Fecha Contrato (AAAA-MM-DD): ").strip()

            exito, msg = self.__controlador.actualizar_empleado(
                id_emp, nom, ape, dir_emp, tel, correo, salario, f_contrato
            )
            print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
        except ValueError:
            print("Ingrese valores numéricos válidos para el ID o Salario.")

    def __eliminar(self):
        print("\n[ Eliminar Empleado ]")
        try:
            id_emp = int(input("ID del empleado a eliminar: "))
            exito, msg = self.__controlador.eliminar_empleado(id_emp)
            print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
        except ValueError:
            print("El ID debe ser un valor entero.")

# --- NOTAS DETALLADAS DEL ARCHIVO (VISTA EMPLEADO) ---
# - __pedir_valido(mensaje, validador, ocultar=False): helper agregado para validar campo por campo en tiempo real con while True; usa input().strip() o getpass() (si ocultar=True) y vuelve a pedir solo el dato que fallo usando las funciones de utils/validaciones.py.
# - __pedir_opcional_entero(mensaje): helper agregado para campos opcionales numericos (idDep); retorna None si se presiona Enter o valida int() sin botar el formulario.
# - __registrar(): pide cada campo validandolo al momento (nombre sin numeros, telefono chileno, correo, salario, fecha AAAA-MM-DD, usuario, clave y rol) y luego envia todo a ControladorEmpleado.registrar_empleado().
# - __listar(), __actualizar(), __eliminar(): listan empleados, solicitan nuevos datos para actualizar o eliminan por ID entero.
