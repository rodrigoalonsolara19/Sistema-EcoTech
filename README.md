Sistema de Gestión Integral y Seguridad — EcoTech Solutions

Aplicación desarrollada en Python bajo arquitectura modular (MVC + DAO + Servicio) orientada a la gestión operativa, financiera y segura de la empresa:

Control de Acceso Basado en Roles (RBAC):

Portal del Empleado: Consulta restringida únicamente a datos personales.
Portal de Recursos Humanos: Liquidación de sueldos en divisas extranjeras e historial de pagos.
Administración y Gerencia: Gestión de empleados, departamentos, proyectos, asignaciones y registros de tiempo.

Consumo Resiliente de APIs Externas:

Integración con APIs de indicadores económicos chilenos (mindicador.cl y respaldo findic.cl) mediante la librería estándar (urllib.request).
Mecanismo de reintentos con retroceso exponencial (exponential backoff) y conmutación por error (failover) automático.
Persistencia local del historial de consultas en base de datos SQLite.

Seguridad y Criptografía Aplicada:

Autenticación: Hashing de contraseñas de una vía con factor de costo configurable mediante bcrypt y protección contra fuerza bruta con límite de intentos y bloqueo temporal.
Privacidad de datos: Cifrado simétrico autenticado (AES-128-CBC + HMAC con Fernet) para datos sensibles almacenados en disco (salarios, correos, teléfonos y direcciones particulares).
Manejo seguro de errores: Los errores técnicos se registran en una bitácora interna (errores.log) y se presentan mensajes amigables al usuario final sin exponer trazas del sistema.
