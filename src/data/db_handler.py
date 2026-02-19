import sqlite3
import os

DB_NAME = "banco_sol.db"

def inicializar_db():
    """Crea la tabla de usuarios con todos los campos necesarios"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    #Aquí se define la estructura de la tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            documento TEXT UNIQUE NOT NULL,
            tipo_doc TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            clave TEXT  
        )
    ''')
    conn.commit()
    conn.close()

def registrar_usuario(usuario, nombre, documento, tipo_doc, telefono, email, clave):
    """Guarda un nuevo usuario con TODOS sus datos de contacto"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        
        cursor.execute(
            "INSERT INTO usuarios (usuario, nombre, documento, tipo_doc, telefono, email, clave) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (usuario, nombre, documento, tipo_doc, telefono, email, clave)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False #Esto quiere decir que el usuario o el documento ya existen
    finally:
        conn.close()

def buscar_por_cedula(cedula_input):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # .strip() quita espacios y .upper() lo pone en mayúsculas para coincidir con el registro
    limpio = cedula_input.strip().upper() 
    cursor.execute("SELECT * FROM usuarios WHERE documento = ?", (limpio,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def buscar_usuario(usuario_input):
    """Busca un usuario por su nombre de usuario y devuelve sus datos"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario_input,))
    resultado = cursor.fetchone()
    
    conn.close()
    return resultado 

def obtener_clave(usuario_input):
    #Aqui obtiene la clave buscando por el nombre de usuario
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT clave FROM usuarios WHERE usuario = ?", (usuario_input,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado [0] #Devuelve solo el texto de la clave
    return None

def actualizar_contacto(usuario_input, nuevo_telefono=None, nuevo_email=None):
    """Permite editar contacto"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if nuevo_telefono:
        cursor.execute("UPDATE usuarios SET telefono = ? WHERE usuario = ?", (nuevo_telefono, usuario_input))
    
    if nuevo_email:
        cursor.execute("UPDATE usuarios SET email = ? WHERE usuario = ?", (nuevo_email, usuario_input))
        
    conn.commit()
    conn.close()
    return True

def actualizar_clave(usuario_input, nueva_clave):
    #Actualiza la clave del usuario buscando por su nombre de usuario
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", (nueva_clave, usuario_input))
    conn.commit()
    conn.close()
    return True