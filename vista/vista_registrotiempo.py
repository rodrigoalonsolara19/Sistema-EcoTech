from controlador.controlador_registrotiempo import ControladorRegistroTiempo

class VistaRegistroTiempo:
    def __init__(self):
        self.__controlador = ControladorRegistroTiempo()

    def configurar_usuario(self, usuario):
        self.__controlador.configurar_usuario(usuario)

    def menu(self):
        while True:
            print("\n--- REGISTRO DE TIEMPO / HORAS ---")
            print("1. Registrar Horas Trabajadas")
            print("2. Listar Registros de Tiempo")
            print("3. Eliminar Registro de Tiempo")
            print("4. Volver al Menú Principal")
            
            opcion = input("Seleccione una opción (1-4): ").strip()

            if opcion == "1":
                try:
                    fecha = input("Fecha (AAAA-MM-DD): ").strip()
                    horas = input("Horas Trabajadas: ").strip()
                    id_emp = int(input("ID del Empleado: "))
                    id_proy = int(input("ID del Proyecto: "))

                    exito, msg = self.__controlador.registrar_tiempo(fecha, horas, id_emp, id_proy)
                    print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
                except ValueError:
                    print("Formato numérico erróneo en los ID o en las Horas.")
            elif opcion == "2":
                print("\n[ Registros de Tiempo ]")
                regs = self.__controlador.listar_registros()
                if not regs:
                    print("No hay registros de tiempo.")
                else:
                    for r in regs:
                        print(f"ID Registro: {r.idReg} | Fecha: {r.fecha} | Horas: {r.horasTrabajadas}")
            elif opcion == "3":
                try:
                    id_reg = int(input("ID de registro a eliminar: "))
                    exito, msg = self.__controlador.eliminar_registro(id_reg)
                    print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
                except ValueError:
                    print("El ID debe ser entero.")
            elif opcion == "4":
                break
            else:
                print("Opción no válida.")

# --- NOTAS DETALLADAS DEL ARCHIVO (VISTA REGISTRO DE TIEMPO) ---
# - configurar_usuario(usuario): entrega la sesion activa a ControladorRegistroTiempo.
# - menu(): permite registrar horas trabajadas (fecha AAAA-MM-DD, horas, idEmpleado, idProy), listar registros y eliminar por ID; captura ValueError si los IDs no son enteros y delega validacion de fecha y horas al controlador.
