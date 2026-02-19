import smtplib
from email.message import EmailMessage

REMITENTE = "bancosol908@gmail.com"
CLAVE_APP = "vabrdgemzlkzmhsk"

def enviar_codigo_recuperacion(destinatario, codigo):
    """Esto envia un correo con el codigo OTP al usuario."""
    try:
        msg = EmailMessage()
        msg['Subject'] = "Codigo de Recuperacion - Banco Sol"
        msg['From'] = REMITENTE
        msg['To'] = destinatario

        cuerpo_correo = f"""
        Hola,

        Has solicitado recuperar tu clave en Banco Sol.
        Tu codigo de seguridad temporal es: {codigo}

        Por favor, escribe este codigo en el chat para continuar.
        Si no solicitaste este cambio, ignora este mensaje y revisa la seguridad de tu cuenta.
        """ 

        # 2. Esta es la línea mágica que faltaba para agregar el texto:
        msg.set_content(cuerpo_correo)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(REMITENTE, CLAVE_APP)
            servidor.send_message(msg)
        
        # 3. Faltaba avisar que fue un éxito
        return True
    
    except Exception as e:
        print(f"Error critico al enviar correo: {e}")
        return False


# 4. Esta zona debe ir PEGADA al borde izquierdo (fuera de la función)
if __name__ == "__main__":
    print("Probando envio de correo...")
    correo_destino = "duqueaaron2006@gmail.com"
    exito = enviar_codigo_recuperacion(correo_destino, "123456")

    if exito:
        print("¡Correo enviado exitosamente! Revisa tu bandeja de entrada.")
    else:
        print("Falló el envío. Revisa tus credenciales.")
