import re
import math
from datetime import datetime

from utils.validaciones import patronUsuario, validar_clave
from dao.dao_empleado import DAOEmpleado
from dao.dao_departamento import DAODepartamento
from controlador.controlador_base import ControladorBase
from modelo.empleado import Empleado
from modelo.departamento import Departamento
from modelo.usuario import Usuario
from modelo.roles import ADMINISTRADOR, GERENTE, normalizar_rol

patronNombre = r"[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:[ '\-][A-Za-zÁÉÍÓÚáéíóúÑñ]+)*"
patronTelefono = r"(?:\+?56)?[2-9]\d{8}"
patronCorreo = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}"

class ControladorEmpleado(ControladorBase):
    def __init__(self):
        super().__init__()
        self.__dao = DAOEmpleado()
        self.__dao_dep = DAODepartamento()

    def registrar_empleado(self, nom, ape, direccion, telefono, correo, salario, fecha_contrato,
                           id_dep, nombre_usuario, clave, rol):
        
        try:
            actor = self._exigir_gerente()
            if not all((nom.strip(), ape.strip(), correo.strip(), fecha_contrato.strip(),
                        nombre_usuario.strip(), clave)):
                        return False, "Nombre, apellido, correo, contrato y datos de acceso son obligatorios."
            if not re.fullmatch(patronNombre, nom.strip()):
                return False, "El nombre solo puede contener letras."
            if not re.fullmatch(patronNombre, ape.strip()):
                return False, "El apellido solo puede contener letras."
            if not re.fullmatch(patronTelefono, telefono.strip()):
                return False, "El teléfono debe contener solo números (ej: +56912345678)."
            if not re.fullmatch(patronCorreo, correo.strip()):
                return False, "El correo electrónico no tiene un formato válido."
            if not re.fullmatch(patronUsuario, nombre_usuario.strip()):
                return False, "El usuario debe tener de 4 a 20 caracteres (letras, números, _ . -)."
            error_clave = validar_clave(clave)
            if error_clave:
                return False, error_clave
            datetime.strptime(fecha_contrato.strip(), "%Y-%m-%d")
            rol_normalizado = normalizar_rol(rol)
            if rol_normalizado == ADMINISTRADOR and actor.rol != ADMINISTRADOR:
                return False, "Solo un Administrador puede crear cuentas Administrador."
            if rol_normalizado == ADMINISTRADOR:
                return False, "Las cuentas Administrador no se asocian a un empleado."

            salario_num = float(salario)
            if not math.isfinite(salario_num) or salario_num < 0:
                return False, "El salario debe ser un número finito no negativo."

            dep_obj = None
            if id_dep is not None:
                id_dep_num = int(id_dep)
                if not self.__dao_dep.existe(id_dep_num):
                    return False, f"El departamento con ID {id_dep_num} no existe. Créalo primero en el Módulo de Departamentos."
                dep_obj = Departamento(idDep=id_dep_num, nomDep="")

            nuevo_emp = Empleado(
                idEmpleado=None,
                nomEmp=nom.strip(),
                apellidoEmp=ape.strip(),
                direccionEmp=direccion.strip(),
                telefono=telefono.strip(),
                correoEmp=correo.strip(),
                salario=salario_num,
                fechaContrato=fecha_contrato.strip(),
                departamento=dep_obj
            )
            usuario = Usuario(
                clave=clave,
                rol=rol_normalizado,
                nombreUsuario=nombre_usuario.strip(),
            )
            exito = self.__dao.registrar(nuevo_emp, usuario)
            if exito:
                return True, "Empleado y cuenta de acceso registrados exitosamente."
            return False, "No se pudo registrar el empleado; revise correo y nombre de usuario duplicados."
        except PermissionError as e:
            return False, str(e)
        except ValueError as e:
            return False, str(e) if str(e) else "Salario, fecha o ID de departamento no válidos."

    def listar_empleados(self):
        usuario = self._usuario_actual()
        if usuario is None:
            raise PermissionError("Debe iniciar sesión para consultar empleados.")
        if usuario.rol in (ADMINISTRADOR, GERENTE):
            return self.__dao.listar_todos()
        return [usuario.empleado] if usuario.empleado is not None else []

    def actualizar_empleado(self, id_emp, nom, ape, direccion, telefono, correo, salario, fecha_contrato):
        try:
            self._exigir_gerente()
            if not all((nom.strip(), ape.strip(), correo.strip(), fecha_contrato.strip())):
                return False, "Nombre, apellido, correo y fecha de contrato son obligatorios."
            if not re.fullmatch(patronNombre, nom.strip()):
                return False, "El nombre solo puede contener letras."
            if not re.fullmatch(patronNombre, ape.strip()):
                return False, "El apellido solo puede contener letras."
            if not re.fullmatch(patronTelefono, telefono.strip()):
                return False, "El teléfono debe contener solo números (ej: +56912345678)."
            if not re.fullmatch(patronCorreo, correo.strip()):
                return False, "El correo electrónico no tiene un formato válido."
            datetime.strptime(fecha_contrato.strip(), "%Y-%m-%d")
            salario_num = float(salario)
            if not math.isfinite(salario_num) or salario_num < 0:
                return False, "El salario debe ser un número finito no negativo."
            emp = Empleado(
                idEmpleado=int(id_emp),
                nomEmp=nom,
                apellidoEmp=ape,
                direccionEmp=direccion,
                telefono=telefono,
                correoEmp=correo,
                salario=salario_num,
                fechaContrato=fecha_contrato
            )
            exito = self.__dao.actualizar(emp)
            if exito:
                return True, "Empleado actualizado correctamente."
            return False, "No se encontró el ID del empleado especificado."
        except PermissionError as e:
            return False, str(e)
        except ValueError:
            return False, "El ID, salario o fecha de contrato no tiene un formato válido."

    def eliminar_empleado(self, id_emp):
        try:
            actor = self._exigir_gerente()
            id_empleado = int(id_emp)
            if actor.empleado is not None and actor.empleado.idEmpleado == id_empleado:
                return False, "No puede eliminar su propio registro de empleado mientras está en sesión."
            exito = self.__dao.eliminar(id_empleado)
            if exito:
                return True, "Empleado eliminado con éxito."
            return False, "No se encontró un empleado con dicho ID."
        except PermissionError as e:
            return False, str(e)
        except ValueError:
            return False, "El ID debe ser un entero."

# --- NOTAS DETALLADAS DEL ARCHIVO (CONTROLADOR EMPLEADOS) ---
# - registrar_empleado(...): exige _exigir_gerente(), valida campos obligatorios, nombres/apellidos sin numeros (patronNombre), telefono chileno de 9 digitos con +56 opcional ((?:\+?56)?[2-9]\d{8}), correo, usuario (patronUsuario), clave con validar_clave(), fecha AAAA-MM-DD, salario finito >= 0 (math.isfinite), rol valido (prohibiendo crear Admin aqui) y existencia real del departamento antes de guardar empleado + usuario en una sola transaccion.
# - listar_empleados(): si es Gerente/Admin lista todos; si es EMPLEADO devuelve solo su propio registro ([usuario.empleado]).
# - actualizar_empleado(...): valida formato de datos y actualiza el empleado existente por ID.
# - eliminar_empleado(id_emp): exige _exigir_gerente() e impide que un usuario borre su propio registro de empleado mientras esta en sesion.
