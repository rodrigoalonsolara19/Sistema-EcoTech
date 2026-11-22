from controlador.controlador_proyecto import ControladorProyecto

class VistaProyecto:
    def __init__(self):
        self.__controlador = ControladorProyecto()

    def configurar_usuario(self, usuario):
        self.__controlador.configurar_usuario(usuario)

    def menu(self):
        while True:
            print("\n--- GESTIÓN DE PROYECTOS ---")
            print("1. Registrar Proyecto")
            print("2. Listar Proyectos")
            print("3. Actualizar Proyecto")
            print("4. Eliminar Proyecto")
            print("5. Volver al Menú Principal")
            
            opcion = input("Seleccione una opción (1-5): ").strip()

            if opcion == "1":
                nom = input("Nombre del Proyecto: ").strip()
                f_inicio = input("Fecha Inicio (AAAA-MM-DD): ").strip()
                f_fin = input("Fecha Fin (opcional): ").strip() or None
                estado = input("Estado (Activo/Finalizado): ").strip() or "Activo"

                exito, msg = self.__controlador.registrar_proyecto(nom, f_inicio, f_fin, estado)
                print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
            elif opcion == "2":
                print("\n[ Lista de Proyectos ]")
                proyectos = self.__controlador.listar_proyectos()
                if not proyectos:
                    print("No hay proyectos registrados.")
                else:
                    for p in proyectos:
                        print(f"ID: {p.idProy} | Nombre: {p.nomProy} | Inicio: {p.fechaInicio} | Estado: {p.estado}")
            elif opcion == "3":
                try:
                    id_proy = int(input("ID de proyecto a actualizar: "))
                    nom = input("Nuevo Nombre: ").strip()
                    f_inicio = input("Nueva Fecha Inicio (AAAA-MM-DD): ").strip()
                    f_fin = input("Nueva Fecha Fin: ").strip() or None
                    estado = input("Nuevo Estado: ").strip()

                    exito, msg = self.__controlador.actualizar_proyecto(id_proy, nom, f_inicio, f_fin, estado)
                    print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
                except ValueError:
                    print("El ID debe ser numérico.")
            elif opcion == "4":
                try:
                    id_proy = int(input("ID de proyecto a eliminar: "))
                    exito, msg = self.__controlador.eliminar_proyecto(id_proy)
                    print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
                except ValueError:
                    print("El ID debe ser numérico.")
            elif opcion == "5":
                break
            else:
                print("Opción no válida.")

# --- NOTAS DETALLADAS DEL ARCHIVO (VISTA PROYECTO) ---
# - configurar_usuario(usuario): inyecta la sesion activa en ControladorProyecto.
# - menu(): gestiona crear, listar, actualizar y eliminar proyectos; las fechas AAAA-MM-DD, orden cronologico (fechaFin >= fechaInicio) y estado (Activo/Finalizado) se validan en ControladorProyecto.__validar_datos(), mientras la vista captura ValueError en IDs no numericos.
