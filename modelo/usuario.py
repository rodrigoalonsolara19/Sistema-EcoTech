import hashlib
import bcrypt
import hmac


from modelo.roles import normalizar_rol


class Usuario:
    def __init__(self, clave, rol, nombreUsuario, empleado=None):
        self.__clave = clave
        self.__rol = normalizar_rol(rol)
        self.__nombreUsuario = nombreUsuario
        self.__empleado = empleado

    @property
    def clave(self):
        return self.__clave

    @clave.setter
    def clave(self, valor):
        self.__clave = valor

    @property
    def rol(self):
        return self.__rol

    @rol.setter
    def rol(self, valor):
        self.__rol = normalizar_rol(valor)

    @property
    def nombreUsuario(self):
        return self.__nombreUsuario

    @nombreUsuario.setter
    def nombreUsuario(self, valor):
        self.__nombreUsuario = valor

    @property
    def empleado(self):
        return self.__empleado

    @empleado.setter
    def empleado(self, valor):
        self.__empleado = valor

    @staticmethod
    def generar_hash_clave(clave):
        clave_bytes = clave.encode("utf-8")
        if len(clave_bytes) > 72:
            raise ValueError("La contraseña no puede superar los 72 bytes...")
        return bcrypt.hashpw(clave_bytes, bcrypt.gensalt(rounds=12)).decode("utf-8")

    @staticmethod
    def verificar_clave(clave, clave_guardada):
        try:
            if not isinstance(clave_guardada, str):
                return False
            if clave_guardada.startswith(("$2a$", "$2b$", "$2y$")):
                clave_bytes = clave.encode("utf-8")
                if len(clave_bytes) > 72:
                    return False
                return bcrypt.checkpw(clave_bytes, clave_guardada.encode("utf-8"))
            if clave_guardada.startswith("pbkdf2_sha256$"):
                _, iteraciones, salt, hash_guardado = clave_guardada.split("$")
                derivada = hashlib.pbkdf2_hmac(
                    "sha256", clave.encode("utf-8"), bytes.fromhex(salt), int(iteraciones)
                )
                return hmac.compare_digest(derivada.hex(), hash_guardado)
            return False
        except (ValueError, TypeError):
            return False

# --- NOTAS DETALLADAS DEL ARCHIVO (MODELO USUARIO Y BCRYPT) ---
# - __init__ y rol.setter: llaman a normalizar_rol(rol) para garantizar que ningun Usuario se construya con un rol invalido.
# - generar_hash_clave(clave): metodo estatico agregado al migrar a bcrypt. Valida que la clave en UTF-8 no supere 72 bytes (limite de Blowfish/bcrypt) y genera el hash con bcrypt.gensalt(rounds=12).
# - verificar_clave(clave, clave_guardada): verifica hashes bcrypt ($2a$/$2b$/$2y$) con bcrypt.checkpw y conserva verificacion temporal de hashes antiguos pbkdf2_sha256$ mediante hmac.compare_digest (comparacion en tiempo constante) para permitir migracion sin bloquear usuarios antiguos.
