import random
from src.utils.mailer import enviar_codigo_recuperacion
from src.data import db_handler
from src.core import auth


#Memoria temporal para guardar los codigos OTP de cada usuario
memoria_otp = {}

def procesar_mensaje(usuario_nombre, mensaje_usuario):
    """
    Aqui esta funcion reemplaza mi menu_consola.py para la web ya que la web no permite
    input ni print eso es solo para la consola.
    """

    #Aqui normalizamos que el mensaje este todo en minisculas y sin espacios extras.

    msg = mensaje_usuario.lower().strip()

    #Caso 1. Aqui se hace el Menu principal 

    match msg:

     #Aqui El chat bot saluda y se despliega el menu principal

     case "menu" | "menú" | "hola" | "inicio" | "volver" | "salir": #El '|' aqui funciona como un "OR"
          return (
                f"Hola <b>{usuario_nombre}</b>, soy Sol ☀️.<br>"
                "Selecciona una opción escribiendo el número:<br><br>"
                "<b>1.</b> Gestión de Claves 🔑<br>"
                "<b>2.</b> Gestión de Usuario (Perfil) 👤<br>"
                "<b>3.</b> Adios"
            )
        
    #Caso 2. Menu de gestion de claves
       
     case "1" | "claves" | "gestion de claves":
          return (
                "<b>=== GESTIÓN DE CLAVES ===</b><br>"
                "¿Qué deseas hacer?<br><br>"
                "🔹 Escribe: <b>'Olvide Clave</b></br>"
                "🔹 Escribe: <b>'Cambiar clave [actual] [nueva]</b>"
            )
    #Caso 3. Menu de usuario   
     case "2" | "perfil" | "usuario":
            return (
                "<b>=== MI PERFIL DE USUARIO ===</b><br>"
                "Elige una opción escribiendo:<br><br>"
                "🔹 <b>'Consultar datos'</b><br>"
                "🔹 <b>'Actualizar telefono [nuevo]'</b><br>"
                "🔹 <b>'Actualizar correo [nuevo]'</b>"
            )
        
    #Caso 4. Salida
     case "3" | "ayuda" | "chao" | "adios":
            return "Hasta pronto! Escribe <b>'menu'</b> cuando quieras volver"
         
    #Caso 5: Comandos complejos (Usando GUARDS)

    #A. Olvide clave

     case _ if "olvide clave" in msg:
              
              #1. buscamos los datos del ususario en la base de datos

              datos_usuario = db_handler.buscar_usuario(usuario_nombre)

              if datos_usuario:
                    #2. extraemos el correo real de la base de datos
                    correo_destino = datos_usuario[6] 

                    #3. Generamos el codigo aleatorio con la libreria random
                    codigo_otp = str(random.randint(100000, 999999))

                    #4. Enviamos el correo a la direccion real
                    exito = enviar_codigo_recuperacion(correo_destino, codigo_otp)
                    print(f"Sol: Resultado del envio: {exito}")

                    if exito:
                         #Aqui guardamos el codigo en la memoia del chatbot
                         memoria_otp[usuario_nombre] = codigo_otp

                         #Ocultmos un poco el correo por privacidad (Ej:yese***@gmail.com)
                         correo_oculto = correo_destino[:4] + "***" + correo_destino[correo_destino.find("@"):]

                         return f"""
                         Tranquilo, <b>{usuario_nombre}</b>.<br>
                         Hemos verificado tu usuario correctamente.<br><br>
                         ✅<b>Hemos enviado un código de recuperación a tu correo registrado ({correo_oculto}).</b><br>
                         Por favor, revisa tu bandeja de entrada y escríbelo aquí:
                         """
                    else:
                          return f"""
                          Lo siento, <b>{usuario_nombre}</b>. Tuvimos un problema técnico
                          al intentar enviar el correo. Por favor, intenta de nuevo más tarde.
                          """
              else:
                   return "Error: No pudimos encontrar tus datos en el sistema"
              


             
     #Caso A.2: Validar el codigo de 6 digitos

     case _ if msg.isdigit() and len(msg) == 6 and memoria_otp.get(usuario_nombre) == msg:
                
                #Borramos el codigo de la memoria (Regla estricta del OTP)
                memoria_otp.pop(usuario_nombre)

                #Aqui confirmamos la identidad del usuario
                return f"""
                <b> Identidad verificada con exito!</b><br><br>
                Tu codigo de verificacion es correcto. ahora puedes reestablecer tu nueva clave.<br>
                Como olvidaste tu clave actual, usa este comando especial para hacer el cambio: <br><br>
                🔹 <b>Recuperar clave [tu_nueva_clave]</b>
                """
          

     #Caso A.3: Guardar la nueva clave en la Base de datos

     case _ if "recuperar clave" in msg:
               palabras = mensaje_usuario.split()

               #Esperamos 3 palabras: "recuperar", "clave" y "la_nueva_clave"

               if len(palabras) == 3:
                     clave_nueva = palabras[2] #Tomamos la tercera palabra

                     #Reutilizamos el sistema de seguridad de auth.py
                     valido, error = auth.validar_clave(clave_nueva)

                     if valido:
                         #Guardamos la nueva clave en la base de datos

                         db_handler.actualizar_clave(usuario_nombre, clave_nueva)

                         return """
                         <b>¡Clave restablecida con éxito!</b><br><br>
                         Tu nueva contraseña ha sido guardada de forma segura en nuestro sistema.<br>
                         Ya puedes utilizarla en tu próximo inicio de sesión.<br><br>
                         Escribe <b>'Menu'</b> para volver a las opciones principales.
                         """
                     else:
                         return f"La clave no es segura: {error}"
               else:
                     return "Formato incorrecto. Escribe <b>Recuperar clave [nueva_clave]</b>"

    #B. Cambiar clave
     case _ if "cambiar clave" in msg:
            palabras = msg.split()
            if len(palabras) == 4:
                clave_vieja = palabras[2]
                clave_nueva = palabras[3]

                clave_real = db_handler.obtener_clave(usuario_nombre)

                if clave_vieja == clave_real:
                     valido, error = auth.validar_clave(clave_nueva)
                     if valido:
                        db_handler.actualizar_clave(usuario_nombre, clave_nueva)
                        return f"✅ Éxito! Tu Clave ha sido actualizada correctamente."
                     else:
                        return f"La clave nueva no es segura: {error}"
                else:
                    return "❌ Error: La clave actual es incorrecta"
            else:
                return "Formato incorrecto. Escribe <b>Cambiar clave [vieja] [nueva]</b>"
            
    #C. Ver Datos

     case _ if "ver mis datos" in msg or "consultar" in msg:
              datos = db_handler.buscar_usuario(usuario_nombre)
              if datos:
                   return(
                    f"<b>--- FICHA DE CLIENTE ---</b><br>"
                    f"👤 Nombre: {datos[2]}<br>"
                    f"🆔 Usuario: {datos[1]}<br>"
                    f"📄 Documento: {datos[3]}<br>"
                    f"📞 Teléfono: {datos[5]}<br>"
                    f"📧 Email: {datos[6]}" 
                   )
              else:
                   return "Error al recuperar datos."
              
    #D. Actualizar Telefono

     case _ if "actualizar telefono" in msg or "cambiar telefono" in msg:
              palabras = msg.split()
              if len(palabras) >= 3:
                   nuevo_tlf = palabras[-1]
                   valido, error = auth.validar_telefono(nuevo_tlf)
                   if valido:
                        db_handler.actualizar_contacto(usuario_nombre, nuevo_telefono = nuevo_tlf)
                        return f"Exito! Telefono actualizado a <b>{nuevo_tlf}</b>"
                   else:
                        return f"{error}"
              else:
                   return "Escribe: <b>Actualizar telefono 0412...</b>"
              
     #E, Actualizar Correo        

     case _ if "actualizar correo" in msg or "cambiar correo" in msg:
              palabras = msg.split()
              if len(palabras) >= 3:
                   nuevo_mail = palabras[-1]
                   valido, error = auth.validar_email(nuevo_mail)
                   if valido:
                        db_handler.actualizar_contacto(usuario_nombre, nuevo_email = nuevo_mail)
                        return f"Exito!: Correo actualizado a <b>{nuevo_mail}</b>"
                   else:
                        return f"{error}"
              else:
                   return "Escribe: <b>Actualizar correo x@gmail.com</b>"
              
     case _:
              return "No entendi esa opcion. Escribe <b>'Menu'</b> para ver las opciones disponibles." 
