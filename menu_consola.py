import sys
import os 
from src.data import db_handler
from src.core import auth


def menu_claves(usuario_actual, documento_actual):
    while True:
        print("\n" + "=" * 30)
        print("   GESTION DE CLAVES")
        print("=" * 30)
        print("1. Clave Telefonica")
        print("2. Clave Internet")
        print("3. Volver al menu principal")

        opcion = input("\nSelecciona una opcion (1-3): ")

        if opcion == "3":
            break 

        nombre_clave = ""
        if opcion == "1":
            nombre_clave = "Clave Telefonica"
        elif opcion == "2":
            nombre_clave = "Clave Internet"
        else:
            print("Opcion no valida.")
            input("(Presiona Enter para intentar de nuevo...)")
            continue
            
        print("-" * 30)
        print(f"   OPCIONES: {nombre_clave.upper()}")
        print("-" * 30)
        print("1. Olvide clave")
        print("2. Cambiar clave")
        print("3. Cancelar")

        sub_opcion = input("\n> Selecciona: ")

        if sub_opcion == "1":
            print(f"\n[Sol]: Olvidaste tu {nombre_clave}? Tranquilo.")
            print("Solo necesitas tu usuario del banco.")

            inicio = input("\nEmpezamos? (Si/No): ").lower().strip()

            if inicio in ["si", "s", "sí", "y"]:
                verificacion = input("Ingresa tu usuario del banco: ")

                if verificacion.strip().lower() == usuario_actual.lower():
                    print(f"\nExito: Usuario verificado correctamente ({usuario_actual}).")
                    print(f"Hemos enviado el codigo de recuperacion a tu correo")
                else:
                    print(f"\nError: El usuario '{verificacion}' no coincide con nuestros registros")
                
                input("\n(Presiona Enter para continuar...)")
            else:
                print("\nEsta bien, cancelando operacion.")
                input("(Presiona Enter para volver...)")

        elif sub_opcion == "2":
            print(f"\n--- CAMBIAR {nombre_clave.upper()} ---")
            clave_actual = input("Ingrese su clave actual: ")

            clave_real_bd = db_handler.obtener_clave(documento_actual)

            if clave_actual == clave_real_bd:
                #Si coincide, pedimos la nueva
                nueva_clave = input("Ingrese su NUEVA clave: ")
                valido, msg = auth.validar_clave(nueva_clave)

                if valido:
                    db_handler.actualizar_clave(documento_actual, nueva_clave)
                    print(f"Exito! Tu {nombre_clave} ha sido actualizada.")
                else:
                    print(f"n{msg}")
            else: 
                print("Error: La clave actual es incorrecta.")

            input("(Presiona Enter para volver...)")

        elif sub_opcion == "3":
            pass 
        else:
            print("Opcion no valida.")
            input("(Presiona Enter para intentar de nuevo...)")

def menu_usuario(usuario_actual, documento_actual):
    while True:
        print("\n" + "=" * 30)
        print("   MI PERFIL DE USUARIO")
        print("=" * 30)
        print("1. Consultar mis datos")
        print("2. Actualizar informacion de contacto")
        print("3. Volver al menu principal")

        opcion = input("\nSelecciona una opcion (1-3): ")

        if opcion == "3":
            break
        
        elif opcion == "1":
            datos = db_handler.buscar_usuario(documento_actual)
            # datos = (nombre, documento, telefono, email)
            
            print(f"\n--- FICHA DE CLIENTE ---")
            if datos:
                print(f"Nombre:    {datos[0]}")
                print(f"Documento: {datos[1]}")
                print(f"Telefono:  {datos[2]}")
                print(f"Email:     {datos[3]}")
            else:
                print("Error al recuperar datos.")
            print("-" * 27)
            input("\n(Presiona Enter para volver...)")

        elif opcion == "2":
            print("\n--- ACTUALIZAR DATOS ---")
            print("1. Telefono")
            print("2. Correo Electronico")
            
            sub_op = input("\n> Elige (1-2) o Enter para cancelar: ")
            
            if sub_op == "1":
                nuevo_tlf = input("Ingresa tu nuevo numero: ")
                # Validamos antes de guardar
                valido, msg = auth.validar_telefono(nuevo_tlf)
                if valido:
                    db_handler.actualizar_contacto(documento_actual, nuevo_telefono=nuevo_tlf)
                    print("Exito: Telefono actualizado!")
                else:
                    print(msg)
                input("(Enter para continuar)")
                
            elif sub_op == "2":
                nuevo_mail = input("Ingresa tu nuevo correo: ")
                valido, msg = auth.validar_email(nuevo_mail)
                if valido:
                    db_handler.actualizar_contacto(documento_actual, nuevo_email=nuevo_mail)
                    print("Exito: Correo actualizado!")
                else:
                    print(msg)
                input("(Enter para continuar)")
            else:
                pass 

        else:
            print("Opcion no valida.")
            input("(Enter para intentar de nuevo)")

def mostrar_menu():
    print("\n" + "="*30)
    print("   MENU DE FUNCIONALIDADES")
    print("="*30)
    print("1. Gestion de Claves")
    print("2. Gestion de Usuario")
    print("3. Salir")
    return input("\nSeleccione una opcion (1-3): ")

def main():
    db_handler.inicializar_db() 

    print("Hola, soy Sol!")
    print("Por favor indicame tus datos de identidad para comenzar.")
    print("(Ejemplos: V-12345678, E-765432189, J-1234567890)")

    usuario_actual = ""
    documento_final = "" # Variable importante para pasarla a los menús

    while True:
        entrada = input("\n> Ingresa tu identificador: ")

        valido, tipo, numero, msg = auth.validar_identificador(entrada)

        if not valido:
            print(msg)
            continue

        documento_final = f"{tipo}-{numero}"
        datos = db_handler.buscar_usuario(documento_final)

        if datos:
            usuario_actual = datos[0]
            print(f"\nBienvenido de nuevo, {usuario_actual}!")
            input("(Presiona Enter para entrar al sistema...)")
            break
        else:
            print("\nParece que eres nuevo.")
            print("Vamos a crear tu perfil de cliente.")
            
            # --- REGISTRO CON VALIDACIONES ---
            
            # 1. Nombre
            while True:
                nombre = input("1. Como te llamas?: ").strip()
                if len(nombre) > 2:
                    break
                print("Por favor escribe un nombre valido.")

            # 2. Telefono (Validado)
            while True:
                telefono = input("2. Ingresa tu numero de telefono (Ej: 04121234567): ").strip()
                valido_tlf, msg_tlf = auth.validar_telefono(telefono)
                if valido_tlf:
                    break 
                print(msg_tlf) 

            # 3. Email (Validado)
            while True:
                email = input("3. Ingresa tu correo: ").strip()
                valido_mail, msg_mail = auth.validar_email(email)
                if valido_mail:
                    break
                print(msg_mail)
            
            # 4. Clave (Validado)
            while True:
                clave = input("4. Crea tu clave de internet (Min 6 caracteres): ")
                valido_clave, msg_clave = auth.validar_clave(clave)
                if valido_clave: break
                print(msg_clave)

            # Guardar en BD
            if db_handler.registrar_usuario(nombre, documento_final, tipo, telefono, email, clave):
                print(f"Felicidades te has registrado exitosamente!")
                usuario_actual = nombre
                input("(Presiona Enter para continuar...)")
                break
            else:
                print("Error al registrar!")

    print(f"\nHola {usuario_actual}! Soy Sol.")

    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            menu_claves(usuario_actual, documento_final)
            
        elif opcion == '2':
            # Pasamos nombre Y documento
            menu_usuario(usuario_actual, documento_final)
            
        elif opcion == '3':
            print(f"\nHasta pronto {usuario_actual}! Esperare tu regreso")
            break
        else:
            print("Opcion no valida.")
            input("(Presiona Enter para intentar de nuevo...)")

if __name__ == '__main__':
    main()