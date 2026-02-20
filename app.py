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

    # Buscamos en la DB. n
    usuario_encontrado = db_handler.buscar_por_cedula(texto_recibido)

    if usuario_encontrado:
        # usuario_encontrado[1] suele ser el NOMBRE en tu estructura
        nombre_usuario = usuario_encontrado[1]
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

        # 1. Armamos el texto completo para tu validador
        texto_a_validar = f"{tipo}-{cedula_num}"

        # 2. Validamos el identificador
        es_valido, tipo_detectado, numero_detectado, mensaje_error = auth.validar_identificador(texto_a_validar)

        if not es_valido:
            flash(mensaje_error) 
            # 💡 TRUCO: Volvemos a renderizar la página enviando los datos previos
            return render_template('registro.html', datos=request.form)

        # 3. Reconstruimos el documento final
        documento_final = f"{tipo_detectado}-{numero_detectado}"

        # Validaciones restantes
        valido_tlf, msg_tlf = auth.validar_telefono(telefono)
        if not valido_tlf:
            flash(msg_tlf)
            return render_template('registro.html', datos=request.form)

        valido_mail, msg_mail = auth.validar_email(email)
        if not valido_mail:
            flash(msg_mail)
            return render_template('registro.html', datos=request.form)
            
        valido_clave, msg_clave = auth.validar_clave(clave)
        if not valido_clave:
            flash(msg_clave)
            return render_template('registro.html', datos=request.form)

        # 4. Guardado en base de datos
        if db_handler.registrar_usuario(usuario, nombre, documento_final, tipo, telefono, email, clave):
            flash("¡Registro exitoso! Ahora inicia sesión con tu USUARIO.")
            # Aquí SÍ usamos redirect porque el registro fue un éxito y lo mandamos al login
            return redirect(url_for('login'))
        else:
            flash("Error: Ese Usuario ya está registrado.")
            return render_template('registro.html', datos=request.form)

    # Si entra por GET (la primera vez que abre la página), enviamos 'datos' vacío
    return render_template('registro.html', datos={})

# 3. RUTA DASHBOARD
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