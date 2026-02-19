import os
import sqlite3
from src.data import db_handler

DB_FILE = "banco_sol.db"

# 1. FORZAR ELIMINACIÓN DE LA BASE DE DATOS
if os.path.exists(DB_FILE):
    try:
        os.remove(DB_FILE)
        print(f"✅ Archivo '{DB_FILE}' eliminado correctamente.")
    except PermissionError:
        print(f"❌ ERROR: No se pudo borrar '{DB_FILE}'. Cierra todas las terminales y VS Code, y vuelve a intentar.")
        exit()
else:
    print(f"ℹ️ El archivo '{DB_FILE}' no existía (eso es bueno).")

# 2. CREAR LA NUEVA BASE DE DATOS
print("🔄 Creando nueva base de datos...")
try:
    db_handler.inicializar_db()
    print("✅ Base de datos inicializada.")
except Exception as e:
    print(f"❌ Error al inicializar: {e}")
    exit()

# 3. VERIFICAR QUE LA COLUMNA 'USUARIO' EXISTE
try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Pedimos información de la tabla usuarios
    cursor.execute("PRAGMA table_info(usuarios)")
    columnas = cursor.fetchall()
    conn.close()

    # Buscamos si existe la columna 'usuario'
    nombres_columnas = [col[1] for col in columnas]
    if 'usuario' in nombres_columnas:
        print("🎉 ¡ÉXITO! La tabla se creó con la columna 'usuario'.")
        print(f"Columnas detectadas: {nombres_columnas}")
    else:
        print("⚠️ FALLO CRÍTICO: La tabla se creó, pero NO tiene la columna 'usuario'.")
        print("Revisa tu archivo src/data/db_handler.py y asegúrate de haberlo GUARDADO.")
        print(f"Columnas actuales: {nombres_columnas}")

except Exception as e:
    print(f"❌ Error al verificar: {e}")