import time
from getpass import getpass
from controlador.controlador_usuario import ControladorUsuario
from utils.registro import logger
from modelo.roles import ADMINISTRADOR
from utils.validaciones import validar_clave, validar_usuario


class VistaUsuario:
    def __init__(self):
        self.__controlador = ControladorUsuario()
        self.__usuario_actual = None

    def configurar_usuario(self, usuario):
        self.__usuario_actual = usuario
        self.__controlador.configurar_usuario(usuario)

    def hay_administradores(self):
        return self.__controlador.hay_administradores()

    def crear_administrador_inicial(self):
        print("\n--- CONFIGURACIÓN INICIAL ---")
        print("No existe una cuenta Administrador. Cree una para iniciar sesión.")
        while True:
            nombre_usuario = input("Nombre de usuario: ").strip()
            clave = getpass("Contraseña (mínimo 14 caracteres): ")
            confirmacion = getpass("Repita la contraseña: ")
            if clave != confirmacion:
                print("Las contraseñas no coinciden.")
                continue
            exito, mensaje = self.__controlador.registrar_administrador_inicial(nombre_usuario, clave)
            print(mensaje)
            if exito:
                return
            if self.__controlador.hay_administradores():
                return

    def autenticar(self):
        intentos = 0
        while True:
            print("\n--- INICIO DE SESIÓN ---")
            nombre_usuario = input("Usuario: ").strip()
            clave = getpass("Contraseña: ")
            try:
                usuario, mensaje = self.__controlador.iniciar_sesion(nombre_usuario, clave)
            except RuntimeError as e:
                logger.error("Error de autenticación: %s", e)
                print("No se pudo iniciar sesión por un error interno. Revise el registro de errores, porfavor...")
                return None
            if usuario is not None:
                print(f"Bienvenido/a, {usuario.nombreUsuario} ({usuario.rol}).")
                return usuario
            print(mensaje)
            intentos += 1
            if intentos >= 3:
                print("Demasiados intentos fallidos. Espere 30 segundos.")
                time.sleep(30)
                intentos = 0

    def menu(self):
        while True:
            print("\n--- GESTIÓN DE USUARIOS ---")
            print("1. Registrar Usuario")
            print("2. Listar Usuarios")
            print("3. Eliminar Usuario")
            print("4. Volver al Menú Principal")
            opcion = input("Seleccione una opción (1-4): ").strip()

            if opcion == "1":
             while True:
                 nombre_usuario = input("Nombre de usuario: ").strip()
                 error = validar_usuario(nombre_usuario)
                 if error is None:
                     break
                 print(f"Incorrecto: {error}")
             while True:
                 clave = getpass("Contraseña (mínimo 14 caracteres): ")
                 error = validar_clave(clave)
                 if error is None:
                     break
                 print(f"Incorrecto: {error}")
             roles = {"1": "EMPLEADO", "2": "GERENTE", "3": "RRHH"}
             if self.__usuario_actual.rol == ADMINISTRADOR:
                 roles["4"] = ADMINISTRADOR
             while True:
                 print("Rol: 1. Empleado  2. Gerente  3. RRHH")
                 if self.__usuario_actual.rol == ADMINISTRADOR:
                     print("4. Administrador")
                 rol_opcion = input("Seleccione el rol: ").strip()
                 if rol_opcion in roles:
                     break
                 print("Incorrecto: Rol no válido.")
             id_emp = None
             if roles[rol_opcion] != ADMINISTRADOR:
                 while True:
                     id_emp_in = input("ID de empleado asociado (opcional): ").strip()
                     if not id_emp_in:
                         break
                     try:
                         id_emp = int(id_emp_in)
                         break
                     except ValueError:
                         print("Incorrecto: El ID de empleado debe ser un entero.")
             exito, msg = self.__controlador.registrar_usuario(
                 nombre_usuario, clave, roles[rol_opcion], id_emp
             )
             print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
             
            elif opcion == "2":
                usuarios = self.__controlador.listar_usuarios()
                if not usuarios:
                    print("No existen usuarios para mostrar.")
                else:
                    for usuario in usuarios:
                        empleado = usuario.empleado
                        asociado = (
                            f" | Empleado: {empleado.nomEmp} {empleado.apellidoEmp}"
                            if empleado else " | Sin empleado asociado"
                        )
                        print(f"Usuario: {usuario.nombreUsuario} | Rol: {usuario.rol}{asociado}")
            elif opcion == "3":
                nombre_usuario = input("Nombre de usuario a eliminar: ").strip()
                exito, msg = self.__controlador.eliminar_usuario(nombre_usuario)
                print(f"{'Correcto' if exito else 'Incorrecto'} {msg}")
            elif opcion == "4":
                break
            else:
                print("Opción no válida.")

# --- NOTAS DETALLADAS DEL ARCHIVO (VISTA USUARIOS) ---
# - configurar_usuario(usuario): pasa la sesion autenticada a ControladorUsuario para validar permisos.
# - hay_administradores() / crear_administrador_inicial(): se llaman en main.py si la BD arranca vacia; piden clave oculta con getpass() y confirmacion.
# - autenticar(): bucle de inicio de sesion con getpass(); tras 3 fallos bloquea 30 segundos (time.sleep(30)) contra fuerza bruta. Ante RuntimeError registra en errores.log (logger.error) y muestra mensaje seguro.
# - menu() opcion 1 (Registrar Usuario): valida al instante en bucles while True usando validar_usuario(), validar_clave(), seleccion de rol (solo Admin ve opcion 3) y entero opcional para idEmpleado sin sacar al usuario del formulario.
# - menu() opciones 2 y 3: listan usuarios (mostrando empleado asociado si existe) y permiten eliminar cuentas via ControladorUsuario.

