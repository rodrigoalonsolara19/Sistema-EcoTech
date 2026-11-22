from utils.config import cargar_env
cargar_env()
from conex.conn import ConexionBD
from vista.vista_indicadores import VistaIndicadores
from modelo.roles import EMPLEADO, RRHH
from vista.vista_empleado import VistaEmpleado
from vista.vista_departamento import VistaDepartamento
from vista.vista_usuario import VistaUsuario
from vista.vista_proyecto import VistaProyecto
from vista.vista_asignacionproyecto import VistaAsignacionProyecto
from vista.vista_registrotiempo import VistaRegistroTiempo
from vista.vista_rrhh import VistaRRHH



def mostrar_perfil(usuario):
    empleado = usuario.empleado
    print("\n--- MI PERFIL ---")
    if empleado is None:
        print("La cuenta no tiene un empleado asociado.")
        return
    print(f"ID: {empleado.idEmpleado}")
    print(f"Nombre: {empleado.nomEmp} {empleado.apellidoEmp}")
    print(f"Correo: {empleado.correoEmp}")
    print(f"Telefono: {empleado.telefono}")
    print(f"Salario: ${empleado.salario:,.2f}")
    print(f"Fecha de contrato: {empleado.fechaContrato}")


def main():
    db = ConexionBD()
    db.inicializar_tablas()

    v_empleado = VistaEmpleado()
    v_departamento = VistaDepartamento()
    v_usuario = VistaUsuario()
    v_proyecto = VistaProyecto()
    v_asignacion = VistaAsignacionProyecto()
    v_registro_tiempo = VistaRegistroTiempo()
    v_indicadores = VistaIndicadores()
    v_rrhh = VistaRRHH()

    if not v_usuario.hay_administradores():
        v_usuario.crear_administrador_inicial()

    while True:
        usuario = v_usuario.autenticar()
        if usuario is None:
            return
        v_empleado.configurar_usuario(usuario)
        v_departamento.configurar_usuario(usuario)
        v_usuario.configurar_usuario(usuario)
        v_proyecto.configurar_usuario(usuario)
        v_asignacion.configurar_usuario(usuario)
        v_indicadores.configurar_usuario(usuario)
        v_registro_tiempo.configurar_usuario(usuario)
        v_rrhh.configurar_usuario(usuario)

        # --- Portal del Empleado (rol EMPLEADO) ---
        if usuario.rol == EMPLEADO:
            while True:
                print("\n--- PORTAL DEL EMPLEADO ---")
                print("1. Ver mis datos")
                print("2. Cerrar sesión")
                print("3. Salir del sistema")
                opcion = input("Seleccione una opción (1-3): ").strip()
                if opcion == "1":
                    mostrar_perfil(usuario)
                elif opcion == "2":
                    break
                elif opcion == "3":
                    return
                else:
                    print("Opción no válida.")
            continue

        # --- Portal de Recursos Humanos (rol RRHH) ---
        if usuario.rol == RRHH:
            while True:
                print("\n" + "=" * 50)
                print("  PORTAL DE RECURSOS HUMANOS — ECOTECH SOLUTIONS")
                print(f"  Sesión: {usuario.nombreUsuario} | Rol: {usuario.rol}")
                print("=" * 50)
                print("1. Módulo de Recursos Humanos")
                print("2. Cerrar sesión")
                print("3. Salir del sistema")
                print("=" * 50)
                opcion = input("Seleccione una opción (1-3): ").strip()
                if opcion == "1":
                    v_rrhh.menu()
                elif opcion == "2":
                    break
                elif opcion == "3":
                    return
                else:
                    print("Opción inválida.")
            continue

        # --- Menú Administrador / Gerente ---
        while True:
            print("\n" + "=" * 50)
            print("  SISTEMA DE GESTIÓN INTEGRAL - ECOTECH SOLUTIONS")
            print(f"  Sesión: {usuario.nombreUsuario} | Rol: {usuario.rol}")
            print("=" * 50)
            print("1. Modulo de Empleados")
            print("2. Modulo de Departamentos")
            print("3. Modulo de Usuarios")
            print("4. Modulo de Proyectos")
            print("5. Modulo de Asignación de Proyectos")
            print("6. Modulo de Registro de Tiempo")
            print("7. Indicadores Económicos (API)")
            print("8. Recursos Humanos (Salarios)")
            print("9. Cerrar sesión")
            print("10. Salir del sistema")
            print("=" * 50)
            opcion = input("Seleccione una opción (1-10): ").strip()

            if opcion == "1":
                v_empleado.menu()
            elif opcion == "2":
                v_departamento.menu()
            elif opcion == "3":
                v_usuario.menu()
            elif opcion == "4":
                v_proyecto.menu()
            elif opcion == "5":
                v_asignacion.menu()
            elif opcion == "6":
                v_registro_tiempo.menu()
            elif opcion == "7":
                v_indicadores.menu()
            elif opcion == "8":
                v_rrhh.menu()
            elif opcion == "9":
                break
            elif opcion == "10":
                return
            else:
                print("Opción inválida. Seleccione un numero entre 1 y 10.")

if __name__ == "__main__":
    main()

# --- NOTAS DETALLADAS DEL ARCHIVO (MAIN / PUNTO DE ENTRADA) ---
# - cargar_env() (arriba, antes de importar vistas/servicios): carga .env en os.environ primero.
# - Tres flujos de menú según rol:
#     * EMPLEADO: solo ve sus datos y puede cerrar sesión.
#     * RRHH: accede únicamente al módulo de Recursos Humanos (nómina y pagos).
#     * ADMINISTRADOR/GERENTE: accede a todos los módulos (1-10), incluido RRHH.
# - v_rrhh.configurar_usuario(usuario): entrega el usuario autenticado al panel de RRHH.
