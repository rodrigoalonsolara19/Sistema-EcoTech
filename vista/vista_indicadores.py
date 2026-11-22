from controlador.controlador_Indc import ControladorIndicadores
from utils.validador_api import INDICADORES_PERMITIDOS


class VistaIndicadores:
    def __init__(self):
        self.__controlador = ControladorIndicadores()

    def configurar_usuario(self, usuario):
        self.__controlador.configurar_usuario(usuario)

    def __pedir_indicador(self):
        disponibles = ", ".join(INDICADORES_PERMITIDOS.keys())
        return input(f"Indicador ({disponibles}): ")

    def __mostrar_serie(self, datos, limite=10):
        serie = datos.get("serie", [])
        if not serie:
            print("No hay datos disponibles para esa consulta.")
            return
        print(f"\nIndicador: {datos.get('nombre', '')} ({datos.get('unidad_medida', '')})")
        print(f"Fuente API: {self.__controlador.fuente_usada}")
        for item in serie[:limite]:
            fecha = str(item.get("fecha", ""))[:10]
            valor = item.get("valor", 0)
            print(f"  Fecha: {fecha} --> Valor: {valor:,.2f}")

    def menu(self):
        while True:
            print("\n--- INDICADORES ECONÓMICOS API ---")
            print("1. Consultar últimos valores")
            print("2. Consultar valor por fecha (DD-MM-AAAA)")
            print("3. Consultar serie por año (AAAA)")
            print("4. Convertir monto CLP a divisas/unidades")
            print("5. Ver historial de consultas")
            print("6. Volver al menú principal")

            opcion = input("Seleccione una opción (1-6): ").strip()

            if opcion == "1":
                ind = self.__pedir_indicador()
                print("Consultando servicio externo, por favor espere...")
                datos, msg = self.__controlador.consultar_actuales(ind)
                if datos:
                    self.__mostrar_serie(datos, limite=5)
                    print("Datos guardados en el historial.")
                else:
                    print(f"Incorrecto: {msg}")

            elif opcion == "2":
                ind = self.__pedir_indicador()
                fecha = input("Fecha DD-MM-AAAA: ")
                print("Consultando servicio externo, por favor espere...")
                datos, msg = self.__controlador.consultar_fecha(ind, fecha)
                if datos:
                    self.__mostrar_serie(datos, limite=1)
                    print("Datos guardados en el historial.")
                else:
                    print(f"Incorrecto: {msg}")

            elif opcion == "3":
                ind = self.__pedir_indicador()
                anio = input("Año AAAA: ")
                print("Consultando servicio externo, por favor espere...")
                datos, msg = self.__controlador.consultar_anio(ind, anio)
                if datos:
                    self.__mostrar_serie(datos, limite=10)
                    print("Datos guardados en el historial.")
                else:
                    print(f"Incorrecto: {msg}")

            elif opcion == "4":
                monto = input("Ingrese monto en pesos chilenos (CLP): ")
                print("Consultando servicio externo, por favor espere...")
                conv, msg = self.__controlador.convertir_monto(monto)
                if conv:
                    print(f"\n[ Conversión según {self.__controlador.fuente_usada} ]")
                    for codigo, resultado in conv.items():
                        print(f"  {codigo.upper()}: {resultado:,.4f}")
                else:
                    print(f"Incorrecto: {msg}")

            elif opcion == "5":
                historial = self.__controlador.listar_historial()
                if not historial:
                    print("No hay consultas registradas aún.")
                else:
                    print("\n[ Historial de Consultas API ]")
                    for h in historial[:20]:
                        param = f" | Parámetro: {h['parametro']}" if h["parametro"] else ""
                        print(f"  #{h['id']} | {h['fecha']} | {h['indicador'].upper()} "
                              f"| Tipo: {h['tipo']}{param} | Fuente: {h['fuente']} "
                              f"| Registros: {len(h['serie'])}")

            elif opcion == "6":
                break
            else:
                print("Opción inválida.")

# --- NOTAS DETALLADAS DEL ARCHIVO (VISTA INDICADORES API) ---
# - Muestra "Consultando servicio externo..." antes de cada llamada a la API (feedback al usuario).
# - Si la API principal cae, el controlador/servicio reintenta con la fuente de respaldo en silencio;
#   el usuario solo ve el resultado o un mensaje amigable de error, nunca un traceback.
# - Opción 5 muestra el historial guardado en SQLite (tabla consultaindicador).
# - Opción 4 (Convertir monto) solo la pueden usar Gerente/Admin; RRHH tiene su propio panel en vista_rrhh.

