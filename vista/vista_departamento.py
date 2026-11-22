from controlador.controlador_departamento import ControladorDepartamento

class VistaDepartamento:
    def __init__(self):
        self.__controlador = ControladorDepartamento()

    def configurar_usuario(self, usuario):
        self.__controlador.configurar_usuario(usuario)

    def menu(self):
        while True:
            print("\n--- GESTIÓN DE DEPARTAMENTOS ---")
            print("1. Registrar Departamento")
            print("2. Listar Departamentos")
            print("3. Actualizar Departamento")
            print("4. Eliminar Departamento")
            print("5. Volver al Menú Principal")
            
            opcion = input("Seleccione una opción (1-5): ").strip()

            if opcion == "1":
                nom = input("Nombre del departamento: ").strip()
                exito, msg = self.__controlador.registrar_departamento(nom)
                print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
            elif opcion == "2":
                print("\n[ Lista de Departamentos ]")
                deps = self.__controlador.listar_departamentos()
                if not deps:
                    print("No hay departamentos registrados.")
                else:
                    for d in deps:
                        print(f"ID: {d.idDep} | Nombre: {d.nomDep}")
            elif opcion == "3":
                try:
                    id_dep = int(input("ID del departamento a actualizar: "))
                    nom = input("Nuevo Nombre del departamento: ").strip()
                    exito, msg = self.__controlador.actualizar_departamento(id_dep, nom)
                    print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
                except ValueError:
                    print("El ID debe ser un entero.")
            elif opcion == "4":
                try:
                    id_dep = int(input("ID del departamento a eliminar: "))
                    exito, msg = self.__controlador.eliminar_departamento(id_dep)
                    print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
                except ValueError:
                    print("El ID debe ser un entero.")
            elif opcion == "5":
                break
            else:
                print("Opción no válida.")

# --- NOTAS DETALLADAS DEL ARCHIVO (VISTA DEPARTAMENTO) ---
# - configurar_usuario(usuario): entrega el usuario en sesion a ControladorDepartamento para validar rol Gerente/Admin.
# - menu(): ofrece CRUD completo en consola (1. Registrar, 2. Listar, 3. Actualizar, 4. Eliminar) y captura ValueError cuando se ingresan letras en lugar de un ID numerico entero.
