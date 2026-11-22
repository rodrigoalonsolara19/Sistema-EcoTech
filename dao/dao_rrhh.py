from conex.conn import ConexionBD
from utils.registro import logger
from sqlite3 import Error
from datetime import date


class DAORegistroPago:
    """Persiste los pagos de salario calculados por el módulo de RRHH."""

    def __init__(self):
        self.__conexion_provider = ConexionBD()

    def guardar_pago(self, id_empleado: int, salario_clp: float,
                     valor_uf: float, valor_dolar: float,
                     valor_euro: float, valor_utm: float,
                     fuente: str) -> bool:
        """Registra el pago de salario con conversiones en la tabla registropago."""
        sql = """
            INSERT INTO registropago
                (idEmpleado, salarioCLP, valorUF, salarioUF,
                 valorDolar, salarioDolar, valorEuro, salarioEuro,
                 valorUTM, salarioUTM, fechaPago, fuente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (
                id_empleado,
                salario_clp,
                valor_uf,
                salario_clp / valor_uf if valor_uf else None,
                valor_dolar,
                salario_clp / valor_dolar if valor_dolar else None,
                valor_euro,
                salario_clp / valor_euro if valor_euro else None,
                valor_utm,
                salario_clp / valor_utm if valor_utm else None,
                str(date.today()),
                fuente,
            ))
            conexion.commit()
            return True
        except Error as e:
            logger.error("Error al guardar pago: %s", e)
            return False
        finally:
            conexion.close()

    def listar_pagos(self) -> list[dict]:
        """Retorna el historial de pagos con datos básicos del empleado."""
        sql = """
            SELECT rp.idPago, e.nomEmp, e.apellidoEmp, e.correoEmp,
                   rp.salarioCLP, rp.valorUF, rp.salarioUF,
                   rp.valorDolar, rp.salarioDolar,
                   rp.valorEuro, rp.salarioEuro,
                   rp.valorUTM, rp.salarioUTM,
                   rp.fechaPago, rp.fuente
            FROM registropago rp
            JOIN empleado e ON e.idEmpleado = rp.idEmpleado
            ORDER BY rp.idPago DESC
        """
        pagos = []
        conexion = self.__conexion_provider.obtener_conexion()
        if not conexion:
            return pagos
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            for f in cursor.fetchall():
                pagos.append({
                    "id": f[0],
                    "nombre": f"{f[1]} {f[2]}",
                    "correo": f[3],
                    "salarioCLP": f[4],
                    "valorUF": f[5], "salarioUF": f[6],
                    "valorDolar": f[7], "salarioDolar": f[8],
                    "valorEuro": f[9], "salarioEuro": f[10],
                    "valorUTM": f[11], "salarioUTM": f[12],
                    "fechaPago": f[13],
                    "fuente": f[14],
                })
            return pagos
        except Error as e:
            logger.error("Error al listar pagos: %s", e)
            return []
        finally:
            conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (DAO REGISTRO DE PAGO / RRHH) ---
# - guardar_pago(): calcula salarioUF, salarioDolar, salarioEuro y salarioUTM dividiendo el salarioCLP
#   por cada tipo de cambio actual y los persiste en registropago con la fecha de hoy y la fuente API.
# - listar_pagos(): hace JOIN con empleado para mostrar nombre, correo y todas las conversiones.
