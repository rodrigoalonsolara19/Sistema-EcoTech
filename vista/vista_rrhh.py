from controlador.controlador_rrhh import ControladorRRHH


class VistaRRHH:
    """Panel exclusivo de Recursos Humanos — no requiere rol Administrador."""

    def __init__(self):
        self.__controlador = ControladorRRHH()

    def configurar_usuario(self, usuario):
        self.__controlador.configurar_usuario(usuario)

    # ------------------------------------------------------------------ #
    # Helpers de presentación                                              #
    # ------------------------------------------------------------------ #
    def __separador(self):
        print("-" * 60)

    # ------------------------------------------------------------------ #
    # Menú principal                                                       #
    # ------------------------------------------------------------------ #
    def menu(self):
        while True:
            print("\n" + "=" * 60)
            print("       MÓDULO DE RECURSOS HUMANOS — RRHH")
            print("=" * 60)
            print("1. Ver nómina de empleados (nombre, correo, salario)")
            print("2. Calcular y registrar pago de salario en divisas")
            print("3. Historial de pagos registrados")
            print("4. Volver al menú principal")
            print("=" * 60)

            opcion = input("Seleccione una opción (1-4): ").strip()

            if opcion == "1":
                self.__ver_nomina()
            elif opcion == "2":
                self.__calcular_pago()
            elif opcion == "3":
                self.__ver_historial()
            elif opcion == "4":
                break
            else:
                print("Opción inválida.")

    # ------------------------------------------------------------------ #
    # Submenús                                                             #
    # ------------------------------------------------------------------ #
    def __ver_nomina(self):
        print("\n[ Nómina de Empleados ]")
        datos, error = self.__controlador.ver_salarios()
        if error:
            print(f"Incorrecto: {error}")
            return
        if not datos:
            print("No hay empleados registrados.")
            return
        self.__separador()
        for d in datos:
            print(f"ID: {d['id']} | {d['nombre']} | Correo: {d['correo']} "
                  f"| Salario: ${d['salario']:,.2f} CLP")
        self.__separador()

    def __calcular_pago(self):
        print("\n[ Calcular Pago de Salario en Divisas ]")
        # Mostrar nómina rápida para elegir
        datos, error = self.__controlador.ver_salarios()
        if error:
            print(f"Incorrecto: {error}")
            return
        if not datos:
            print("No hay empleados registrados.")
            return
        self.__separador()
        for d in datos:
            print(f"  ID {d['id']} — {d['nombre']} — ${d['salario']:,.2f} CLP")
        self.__separador()

        id_txt = input("ID del empleado a pagar (Enter para cancelar): ").strip()
        if not id_txt:
            return
        print("Consultando tipos de cambio, por favor espere...")
        resultado, msg = self.__controlador.calcular_pago_empleado(id_txt)
        if resultado is None:
            print(f"Incorrecto: {msg}")
            return

        print(f"\n[ Liquidación de Pago — {resultado['nombre']} ]")
        print(f"  Correo     : {resultado['correo']}")
        print(f"  Salario    : ${resultado['salarioCLP']:>15,.2f} CLP")
        self.__separador()
        for divisa in ("uf", "dolar", "euro", "utm"):
            info = resultado[divisa]
            print(f"  {divisa.upper():<8}: 1 {divisa.upper()} = ${info['valor']:>12,.2f} CLP  "
                  f"→  Salario equivale a {info['equivale']:>12,.4f} {divisa.upper()}")
        self.__separador()
        fuente = self.__controlador.fuente_usada
        print(f"  Fuente API : {fuente}")
        print(f"  Resultado  : {msg}")

    def __ver_historial(self):
        print("\n[ Historial de Pagos Registrados ]")
        pagos, error = self.__controlador.listar_pagos()
        if error:
            print(f"Incorrecto: {error}")
            return
        if not pagos:
            print("No hay pagos registrados aún.")
            return
        self.__separador()
        for p in pagos[:30]:
            print(f"  #{p['id']} | {p['fechaPago']} | {p['nombre']} "
                  f"| Salario: ${p['salarioCLP']:,.2f} CLP "
                  f"| UF: {p['salarioUF']:.4f} | Fuente: {p['fuente']}")
        self.__separador()

# --- NOTAS DETALLADAS DEL ARCHIVO (VISTA RRHH) ---
# - Solo accede quien tenga rol RRHH o ADMINISTRADOR (control en ControladorRRHH).
# - __ver_nomina(): muestra ID, nombre completo, correo y salario CLP de cada empleado.
# - __calcular_pago(): muestra la nómina, pide ID, llama al controlador y presenta la
#   liquidación completa (CLP, UF, Dólar, Euro, UTM) con el tipo de cambio actual de la API.
#   El resultado queda guardado en la tabla registropago de SQLite.
# - __ver_historial(): lista los últimos 30 pagos registrados con fecha y conversiones.
