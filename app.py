from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from src.data import db_handler
from src.core import auth 
from src.core import brain

app = Flask(__name__)
app.secret_key = "clave_secreta_banco_sol"

# 1. RUTA LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_input = request.form['usuario_login'] #Aqui se recibe el usuario
        clave_input = request.form['clave']

        datos_usuario = db_handler.buscar_usuario(usuario_input)
        
        if datos_usuario:
            clave_real = db_handler.obtener_clave(usuario_input)
            if clave_input == clave_real:
                return redirect(url_for('dashboard', nombre=datos_usuario[1]))
            else:
                flash("Contraseña incorrecta")
        else:
            flash("Usuario no encontrado. Revisa tu nombre de usuario.")

    return render_template('login.html')

@app.route('/api/soporte_login', methods=['POST'])
def soporte_login():
    data = request.get_json()
    # Limpiamos el texto que envía el usuario (por si pone espacios)
    texto_recibido = data.get('mensaje', '').strip()

    # Buscamos en la DB. 
    # IMPORTANTE: Asegúrate de que db_handler tenga esta función
    usuario_encontrado = db_handler.buscar_por_cedula(texto_recibido)

    if usuario_encontrado:
        # usuario_encontrado[1] suele ser el NOMBRE en tu estructura
        nombre_usuario = usuario_encontrado[1]
        # Devolvemos la URL a la que el frontend debe redirigir
        # Debe ser asi:
        return jsonify({
            'status': 'encontrado',
            'url': url_for('chat', nombre=nombre_usuario)
        })
    else:
        return jsonify({
            'status': 'error', 
            'mensaje': 'Esa cédula no coincide con nuestros registros. Debe tener el formato correcto (Ej: V-12345678) y estar registrada.'
        })

@app.route('/chat/<nombre>')
def chat(nombre):
    return render_template('chat.html', nombre=nombre)

# 2. RUTA REGISTRO 
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Capturamos datos del formulario web
        usuario = request.form['usuario']
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        cedula_num = request.form['cedula']
        telefono = request.form['telefono']
        email = request.form['email']
        clave = request.form['clave']

        # 1. Armamos el texto completo para tu validador (Ej: "V-12345678")
        texto_a_validar = f"{tipo}-{cedula_num}"

        # 2. Usamos la funcion "validar_identificador" de mi archivo auth.py
        # La función devuelve 4 cosas: (valido, tipo_limpio, numero_limpio, mensaje)
        es_valido, tipo_detectado, numero_detectado, mensaje_error = auth.validar_identificador(texto_a_validar)

        if not es_valido:
            flash(mensaje_error) # Aquí se muestra el mensaje de error ("Error! la cedula debe tener...")
            return redirect(url_for('registro'))

        # 3. Si pasa la prueba, reconstruimos el documento final
        documento_final = f"{tipo_detectado}-{numero_detectado}"

        #Aqui van el resto de validaciones (Teléfono, Email, Clave) ---
        valido_tlf, msg_tlf = auth.validar_telefono(telefono)
        if not valido_tlf:
            flash(msg_tlf)
            return redirect(url_for('registro'))

        valido_mail, msg_mail = auth.validar_email(email)
        if not valido_mail:
            flash(msg_mail)
            return redirect(url_for('registro'))
            
        valido_clave, msg_clave = auth.validar_clave(clave)
        if not valido_clave:
            flash(msg_clave)
            return redirect(url_for('registro'))

        # 4. Aqui se guarda en la base de datos
        if db_handler.registrar_usuario(usuario, nombre, documento_final, tipo, telefono, email, clave):
            flash("¡Registro exitoso! Ahora inicia sesión con tu USUARIO.")
            return redirect(url_for('login'))
        else:
            flash("Error: Esa Usuario ya está registrada.")

    return render_template('registro.html')

# 3. RUTA DASHBOARD
# 3. RUTA DASHBOARD (DESPUES)
@app.route('/dashboard/<nombre>')
def dashboard(nombre):
    return render_template('dashboard.html', nombre = nombre)

#Puente entre el HTML Y BRAIN.PY
@app.route('/api/chat', methods=['POST'])

def chat_api():
    data = request.get_json()
    mensaje = data.get('mensaje')
    usuario = data.get('usuario')


    respuesta = brain.procesar_mensaje(usuario, mensaje)
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    db_handler.inicializar_db() 
    app.run(debug=True, port=5000)