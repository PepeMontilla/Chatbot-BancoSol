Markdown
# 🏦 Banco Sol - Sistema de Gestión Bancaria

## 📄 Descripción
**Banco Sol** es una aplicación de software que simula un sistema bancario interactivo. Permite a los usuarios registrarse, iniciar sesión y gestionar sus perfiles de forma segura a través de dos interfaces:
1. **Web**: Una interfaz moderna construida con Flask que incluye un **Chatbot Inteligente ("Sol")**.
2. **Consola**: Un menú tradicional de línea de comandos (CLI).

**✨ Novedad:** El sistema ahora cuenta con un **Módulo de Seguridad OTP (One-Time Password)**. Si un usuario olvida su contraseña, el chatbot es capaz de consultar su correo en la base de datos y enviarle un código de verificación temporal de 6 dígitos vía SMTP para autorizar el restablecimiento seguro de sus credenciales.

Este proyecto demuestra buenas prácticas de programación en Python, arquitectura modular (MVC), uso de bases de datos SQL y protocolos de seguridad para envíos automatizados por correo electrónico.

## 📂 Estructura del Proyecto

El código está organizado siguiendo el patrón de separación de responsabilidades:

```text
/ (Raíz del proyecto)
├── app.py                 # Servidor Web (Flask) - Punto de entrada Web
├── menu_consola.py        # Interfaz de Consola - Punto de entrada CLI
├── reset_db.py            # Herramienta para reiniciar la Base de Datos
├── banco_sol.db           # Archivo de Base de Datos (SQLite)
└── src/                   # Código Fuente Principal
    ├── core/              # Lógica de Negocio
    │   ├── auth.py        # Validaciones (Cédula, RIF, Email, Claves)
    │   └── brain.py       # Lógica del Chatbot (Procesamiento y Memoria OTP)
    ├── data/              # Acceso a Datos
    │   └── db_handler.py  # Consultas SQL y conexión a la BD
    └── utils/             # Herramientas del Sistema
        └── mailer.py      # Motor de envío de correos (SMTP Google)
⚙️ Configuración Previa (Importante)
Para que el sistema de recuperación de contraseñas funcione correctamente, debes configurar las credenciales de envío de correos:

Abre el archivo src/utils/mailer.py.

Modifica las variables globales con un correo de Gmail válido y una Clave de Aplicación (App Password) generada desde la seguridad de tu cuenta de Google (No uses tu contraseña personal normal):

Python
REMITENTE = "tu_correo@gmail.com"
CLAVE_APP = "tu_clave_de_16_letras_sin_espacios"
🚀 Guía de Instalación y Ejecución
Requisitos Previos
Python 3.10 o superior (necesario para la funcionalidad match-case).

Librería Flask:

Bash
pip install flask
¿Cómo ejecutarlo?
Opción A: Versión Web (Recomendada)
Abre la terminal en la carpeta del proyecto.

Ejecuta el comando:

Bash
python app.py
Abre tu navegador y ve a: http://127.0.0.1:5000

Opción B: Versión de Consola
Ejecuta el comando:

Bash
python menu_consola.py
Sigue las instrucciones en pantalla.

📘 Documentación Técnica Detallada
A continuación se explica la función de cada módulo para facilitar la revisión del código.

1. src/core/auth.py (Módulo de Seguridad)
Contiene funciones puras encargadas de validar la entrada de datos antes de procesarlos en la base de datos.

Identificadores: Detecta y valida Cédulas (V/E) o RIF (J).

Datos de contacto: Usa expresiones regulares (Regex) para correos y valida prefijos telefónicos (0412, 0414, etc.).

Credenciales: Verifica la fortaleza de las contraseñas.

2. src/core/brain.py (Cerebro del Chatbot)
Es el núcleo de la inteligencia y memoria del asistente virtual.

Pattern Matching: Utiliza la estructura match-case de Python para detectar intenciones del usuario, desde comandos simples hasta flujos complejos.

Flujo OTP (Recuperación de Claves): Genera tokens numéricos aleatorios, interactúa con la base de datos para extraer el correo del cliente, ordena el envío a mailer.py y guarda el código en una memoria temporal RAM (memoria_otp) para verificar la identidad del usuario en el siguiente mensaje.

3. src/utils/mailer.py (Módulo de Comunicaciones)
Encargado de las notificaciones externas del sistema.

SMTP SSL: Establece una conexión cifrada por el puerto 465 con los servidores de Google para garantizar la entrega segura de correos electrónicos transaccionales.

4. src/data/db_handler.py (Manejador de Base de Datos)
Encapsula todas las operaciones SQL (SQLite).

CRUD de Usuarios: Maneja el registro, búsqueda de datos (incluyendo correos dinámicos) y actualización de credenciales.

Seguridad SQL: Implementa consultas parametrizadas (?) para prevenir ataques de inyección SQL.

5. app.py (Controlador Web)
Utiliza el framework Flask para servir la aplicación.

Rutas: Maneja el Login (/), Registro de usuarios (/registro) y el área privada del Dashboard (/dashboard/<nombre>).

API REST: Expone el endpoint /api/chat para conectar el frontend dinámico (JS/HTML) con la inteligencia de brain.py de forma asíncrona.