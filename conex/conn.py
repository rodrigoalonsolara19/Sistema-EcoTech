import os
import sqlite3
from pathlib import Path
from utils.registro import logger
from sqlite3 import Error

class ConexionBD:
    def __init__(self, db_name=None):
        self.__db_name = str(db_name or os.getenv("ECOTECH_DB") or Path(__file__).resolve().parent.parent / "ecotech.db")

    def obtener_conexion(self):
        """Establece y retorna la conexión a la base de datos SQLite."""
        try:
            conexion = sqlite3.connect(self.__db_name, timeout=30)
            conexion.execute("PRAGMA journal_mode=WAL;")
            conexion.execute("PRAGMA foreign_keys = ON;")
            return conexion
        except Error as e:
            logger.error("Error al conectar a la Base de Datos '%s': %s", self.__db_name, e)
            return None

    def inicializar_tablas(self):
        """Crea todas las tablas del sistema EcoTech si no existen."""
        conexion = self.obtener_conexion()
        if conexion is not None:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento (
                    idDep INTEGER PRIMARY KEY AUTOINCREMENT,
                    nomDep TEXT NOT NULL
                );
                """)

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleado (
                    idEmpleado INTEGER PRIMARY KEY AUTOINCREMENT,
                    nomEmp TEXT NOT NULL,
                    apellidoEmp TEXT NOT NULL,
                    direccionEmp TEXT,
                    telefono TEXT,
                    correoEmp TEXT UNIQUE NOT NULL,
                    salario REAL NOT NULL,
                    fechaContrato TEXT NOT NULL,
                    idDep INTEGER,
                    FOREIGN KEY (idDep) REFERENCES departamento (idDep) ON DELETE SET NULL
                );
                """)

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    nombreUsuario TEXT PRIMARY KEY,
                    clave TEXT NOT NULL,
                    rol TEXT NOT NULL,
                    idEmpleado INTEGER UNIQUE,
                    FOREIGN KEY (idEmpleado) REFERENCES empleado (idEmpleado) ON DELETE CASCADE
                );
                """)

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyecto (
                    idProy INTEGER PRIMARY KEY AUTOINCREMENT,
                    nomProy TEXT NOT NULL,
                    fechaInicio TEXT NOT NULL,
                    fechaFin TEXT,
                    estado TEXT DEFAULT 'Activo'
                );
                """)

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS asignacionproyecto (
                    idAsProy INTEGER PRIMARY KEY AUTOINCREMENT,
                    fechaAsignacion TEXT NOT NULL,
                    idEmpleado INTEGER NOT NULL,
                    idProy INTEGER NOT NULL,
                    FOREIGN KEY (idEmpleado) REFERENCES empleado (idEmpleado) ON DELETE CASCADE,
                    FOREIGN KEY (idProy) REFERENCES proyecto (idProy) ON DELETE CASCADE
                );
                """)

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS registrotiempo (
                    idReg INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    horasTrabajadas REAL NOT NULL,
                    idEmpleado INTEGER NOT NULL,
                    idProy INTEGER NOT NULL,
                    FOREIGN KEY (idEmpleado) REFERENCES empleado (idEmpleado) ON DELETE CASCADE,
                    FOREIGN KEY (idProy) REFERENCES proyecto (idProy) ON DELETE CASCADE
                );
                """)

                # Tabla para guardar el historial de consultas a la API de indicadores
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS consultaindicador (
                    idConsulta INTEGER PRIMARY KEY AUTOINCREMENT,
                    fechaConsulta TEXT NOT NULL,
                    indicador TEXT NOT NULL,
                    tipoConsulta TEXT NOT NULL,
                    parametro TEXT,
                    fuente TEXT,
                    resultado TEXT NOT NULL
                );
                """)

                # Tabla de registro de pagos de salario (para el módulo de RRHH)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS registropago (
                    idPago INTEGER PRIMARY KEY AUTOINCREMENT,
                    idEmpleado INTEGER NOT NULL,
                    salarioCLP REAL NOT NULL,
                    valorUF REAL,
                    salarioUF REAL,
                    valorDolar REAL,
                    salarioDolar REAL,
                    valorEuro REAL,
                    salarioEuro REAL,
                    valorUTM REAL,
                    salarioUTM REAL,
                    fechaPago TEXT NOT NULL,
                    fuente TEXT,
                    FOREIGN KEY (idEmpleado) REFERENCES empleado (idEmpleado) ON DELETE CASCADE
                );
                """)

                conexion.commit()

                # Crear el departamento "Recursos Humanos" si no existe
                cursor.execute(
                    "SELECT 1 FROM departamento WHERE UPPER(TRIM(nomDep)) = 'RECURSOS HUMANOS' LIMIT 1"
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO departamento (nomDep) VALUES (?)",
                        ("Recursos Humanos",),
                    )
                    conexion.commit()

                print("Estructura completa de Base de Datos inicializada.")
            except Error as e:
                logger.error("Error al crear tablas: %s", e)
            finally:
                conexion.close()

# --- NOTAS DETALLADAS DEL ARCHIVO (CONEXION BD) ---
# - __init__(db_name=None): prioridad: parámetro > ECOTECH_DB (.env) > ecotech.db en raíz.
# - obtener_conexion(): abre la conexión y ejecuta PRAGMA foreign_keys = ON (SQLite lo desactiva por defecto).
# - inicializar_tablas(): crea 8 tablas (+ consultaindicador + registropago) con CREATE TABLE IF NOT EXISTS
#   y crea automáticamente el departamento "Recursos Humanos" si no existe.

