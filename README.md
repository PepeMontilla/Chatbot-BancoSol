# 🏦 Banco Sol - Sistema de Gestión Bancaria

## 📄 Descripción
**Banco Sol** es una aplicación de software que simula un sistema bancario básico. Permite a los usuarios registrarse, iniciar sesión y gestionar sus perfiles (claves, datos de contacto) a través de dos interfaces:
1. **Web**: Una interfaz moderna construida con Flask que incluye un **Chatbot Inteligente ("Sol")**.
2. **Consola**: Un menú tradicional de línea de comandos (CLI).

Este proyecto fue diseñado para demostrar buenas prácticas de programación en Python, arquitectura modular (MVC) y el uso de bases de datos SQL.

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
    │   └── brain.py       # Lógica del Chatbot (Procesamiento de texto)
    └── data/              # Acceso a Datos
        └── db_handler.py  # Consultas SQL y conexión a la BD
```

## 🚀 Guía de Instalación y Ejecución

### Requisitos Previos
*   **Python 3.10** o superior (necesario para la funcionalidad `match-case`).
*   Librería **Flask**:
    ```bash
    pip install flask
    ```

### ¿Cómo ejecutarlo?

#### Opción A: Versión Web (Recomendada)
1.  Abre la terminal en la carpeta del proyecto.
2.  Ejecuta el comando:
    ```bash
    python app.py
    ```
3.  Abre tu navegador y ve a: `http://127.0.0.1:5000`

#### Opción B: Versión de Consola
1.  Ejecuta el comando:
    ```bash
    python menu_consola.py
    ```
2.  Sigue las instrucciones en pantalla.

---

## 📘 Documentación Técnica Detallada

A continuación se explica la función de cada módulo para facilitar la revisión del código.

### 1. `src/core/auth.py` (Módulo de Seguridad)
Este archivo contiene funciones puras encargadas de validar la entrada de datos antes de procesarlos.
*   **`validar_identificador(texto)`**: Detecta si el documento es Cédula (V/E) o RIF (J). Valida que el resto sean números y tengan la longitud correcta.
*   **`validar_email(email)`**: Usa expresiones regulares (Regex) para asegurar el formato `usuario@dominio.com`.
*   **`validar_telefono(telefono)`**: Asegura que sean 11 dígitos y comiencen con prefijos válidos de operadoras venezolanas (0412, 0414, etc.).
*   **`validar_clave(clave)`**: Verifica longitud mínima y ausencia de espacios.

### 2. `src/core/brain.py` (Cerebro del Chatbot)
Es el núcleo de la inteligencia del asistente virtual en la web.
*   **Función `procesar_mensaje`**: Recibe el texto del usuario, lo normaliza y decide qué responder.
*   **Pattern Matching**: Utiliza la estructura `match-case` de Python para detectar comandos simples ("hola", "menu") y complejos ("cambiar clave [vieja] [nueva]").
*   **Integración**: Llama directamente a la base de datos para ejecutar las acciones solicitadas por el chat y devuelve respuestas formateadas en HTML.

### 3. `src/data/db_handler.py` (Manejador de Base de Datos)
Encapsula todas las operaciones SQL (SQLite).
*   **`inicializar_db`**: Crea la tabla `usuarios` automáticamente si no existe.
*   **CRUD de Usuarios**: Funciones para `registrar_usuario`, `buscar_usuario`, `actualizar_clave` y `actualizar_contacto`.
*   **Seguridad**: Usa consultas parametrizadas (`?`) para prevenir inyección SQL.

### 4. `app.py` (Controlador Web)
Utiliza el framework **Flask** para servir la aplicación.
*   **Rutas Principales**:
    *   `/`: Login de usuarios.
    *   `/registro`: Formulario de registro con validaciones visuales (`flash messages`).
    *   `/dashboard/<nombre>`: Área privada donde vive el chat.
    *   `/api/chat`: API JSON que conecta el frontend (HTML/JS) con `brain.py` sin recargar la página.