import re

def validar_identificador(texto_input):
    #Esta funcion se va a encargar de validar si es V-, E- y J-

    texto = texto_input.upper().strip()
    prefijos = ["V-", "E-", "J-"]

    #Aqui se va a verificar el prefijo
    tipo_detectado = None
    for prefijo in prefijos:
        if texto.startswith(prefijo):
            tipo_detectado = prefijo
            break
    
    if not tipo_detectado:
        return False, None, None, "Error: Usa el formato V-, E- o J- seguido del numero del documento."
    
    #Aqui se va a verificar que lo demas sean numeros

    numero_doc = texto.replace(tipo_detectado, "")

    if not numero_doc.isdigit():
        return False, None, None, "Error! Despues del guion solo van numeros"
    
    #Validaciones especificas dependiendo del tipo del documento

    if tipo_detectado == "J-":
        if len(numero_doc) > 10:
            return False, None, None, f"Error!: El RIF debe tener 10 digitos (escribiste {len(numero_doc)})"
        
    else:
        if not (7 <= len(numero_doc) <= 8):
            return False, None, None, "Error! la cedula debe de tener entre 7 y 9 digitos"
            
    return True, tipo_detectado.replace("-", ""), numero_doc, "OK"

def validar_email(email):
    #Aqui verifica que el correo tenga el formato nombre@dominio.com

    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(patron, email):
        return True, ""
    else:
        return False, "Error! El correo debe tener formato 'usuario@dominio.com'"
    
def validar_telefono(telefono):
    #Verifica que sean 11 digitos y empiece por prefijos venezolanos

    #Validamos que sean solo numeros
    
    if not telefono.isdigit():
        return False, "Error: El telefono solo debe contener numeros."
    
    #Que tengan 11 digitos (ejemplo: 04142659832)

    if len(telefono)!= 11:
        return False, f"Error: deben tener 11 digitos. escribiste {len(telefono)}."
    
    #Validamos los prefijos comunes

    prefijos = ['0412', '0422', '0414', '0424', '0416', '0426']
    if not any(telefono.startswith(p) for p in prefijos):
        return False, "Error! Prefijo desconocido. (Usa 0412, 0422, 0414, 0424, 0416, 0426)"
    
    return True, ""

def validar_clave(clave):
    #Verifica que la clave sea segura (Minimo 6 caracteres)

    if len(clave) < 6:
        return False, "Error: La clave debe tener al menos 6 caracteres."
    if " " in clave:
        return False, "Error: La clave no puede tener espacios"
    
    return True, ""

