from controlador.controlador_asignacionproyecto import ControladorAsignacionProyecto

class VistaAsignacionProyecto:
    def __init__(self):
        self.__controlador = ControladorAsignacionProyecto()

    def configurar_usuario(self, usuario):
        self.__controlador.configurar_usuario(usuario)

    def menu(self):
        while True:
            print("\n--- ASIGNACIÓN DE PROYECTOS ---")
            print("1. Asignar Empleado a Proyecto")
            print("2. Listar Asignaciones")
            print("3. Eliminar Asignación")
            print("4. Volver al Menú Principal")
            
            opcion = input("Seleccione una opción (1-4): ").strip()

            if opcion == "1":
                try:
                    f_asig = input("Fecha de Asignación (AAAA-MM-DD): ").strip()
                    id_emp = int(input("ID de Empleado: "))
                    id_proy = int(input("ID de Proyecto: "))

                    exito, msg = self.__controlador.registrar_asignacion(f_asig, id_emp, id_proy)
                    print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
                except ValueError:
                    print("Los ID deben ser valores numéricos enteros.")
            elif opcion == "2":
                print("\n[ Lista de Asignaciones ]")
                asigs = self.__controlador.listar_asignaciones()
                if not asigs:
                    print("No hay asignaciones registradas.")
                else:
                    for a in asigs:
                        print(f"ID Asignación: {a.idAsProy} | Fecha: {a.fechaAsignacion}")
            elif opcion == "3":
                try:
                    id_asig = int(input("ID de asignación a eliminar: "))
                    exito, msg = self.__controlador.eliminar_asignacion(id_asig)
                    print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
                except ValueError:
                    print("El ID debe ser un entero.")
            elif opcion == "4":
                break
            else:
                print("Opción no válida.")

# --- NOTAS DETALLADAS DEL ARCHIVO (VISTA ASIGNACION DE PROYECTO) ---
# - configurar_usuario(usuario): pasa la sesion activa a ControladorAsignacionProyecto.
# - menu(): permite asignar un empleado a un proyecto (pidiendo fecha AAAA-MM-DD e IDs enteros), listar asignaciones o eliminar una por ID; captura ValueError en consola y delega la validacion de fecha al controlador.
