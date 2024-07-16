# Importacion de librerias.
import mysql.connector
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
import flask_login

# Inicializacion de la pagina
app = Flask(__name__)
# Esta linea es delicada ya que sin ella las sessiones no funcionaran.
app.secret_key = 'secret_key'

# Conexion con la base de datos de railway.
mydb = mysql.connector.connect(
    host='roundhouse.proxy.rlwy.net',
    user='root',
    password='alzSPNqOksaVjmzIgLKqqcuiHwCaCFei',
    port=36119,
    database='railway'
)

# Ejecutador de comandos/consultas de la base de datos.
cursor = mydb.cursor()
# ------------------------------------------------------------------------------------------------------------

# Ruta de la pagina principal.


@app.route('/')
def index():
    return render_template('index.html')


# ------------------------------------------------------------------------------------------------------------
"""
# Ruta de la pagina de registro.


@app.route("/register")
def register():
    if session:  # Esta condicional verfica si hay alguna sesion en curso, si es valida no se podrá ingresar a esta ruta, será redirigido al inicio, ya que no se puede registrar un usuario ya registrado.
        return redirect(url_for('inicio'))
    else:  # Si no hay una sesion en curso se autorizará el ingreso a  la pagina de registro.
        return render_template('register.html')
"""

# -----------------------------------------------------------------------------------------------------------

# Ruta para la pagina de login.


@app.route('/login')
def login():
    if session:  # Esta condicional verfica si hay alguna sesion en curso, si es valida no se podrá ingresar a esta ruta, será redirigido al inicio, ya que no puede iniciar sesion un usuario que ya inicio sesion.
        return redirect(url_for('inicio'))
    else:  # Si no hay una sesion en curso se autorizará el ingreso a  la pagina de logueo.
        return render_template('login.html')
# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de incio.


@app.route('/inicio')
def inicio():
    if session:  # Si hay una sesion en curso se podrá accerder al inicio.
        return render_template('inicio.html')
    else:  # Si no hay una sesion en curso se redirigira a la pagina de logueo.
        return redirect(url_for('login'))


# -----------------------------------------------------------------------------------------------------------
"""
# Ruta para el procesamiento del registro.


@app.route('/registering', methods=['GET', 'POST'])
def regitering():
    if request.method == 'POST':
        # Aqui se obtienen todos los valores de los inputs del formulario de "register.html". int y str son para obtener los valores respectivamente en numero entero y tipo texto.
        document = int(request.form['inputDocumentNumber'])
        password = str(request.form['inputPassword'])
        username = str(request.form['inputUsername'])
        email = str(request.form['inputEmail'])
        biography = str(request.form['textareaBiography'])
        # Esta es la ruta de la imagen de perfil por defecto.
        imageProfile = "{{url_for('static', filename='img/ICONS/User_sinFoto.png')}}"

        # Aqui se verifica si se ingreso algun numero de documento y si es el caso se busca ese numero en la base de datos en la tabla MIEMBRO para verficar si esta matriculado en el colegio.
        if document:
            cursor.execute(
                # Se hace una consulta en la base de datos en la tabla MIEMBRO para buscar el numero de documento que ingreso el usuario en el registro.
                "SELECT * FROM MIEMBRO WHERE documentNumber_matricule = %s", (document,))
            # Aqui se obtiene el primer valor arrojado por la consulta en la base de datos.
            miembro_encontrado = cursor.fetchone()

            if miembro_encontrado:
                print("MIEMBRO ENCONTRADO")
                # Con el documento ya verificado, tambn se verifica el nombre de usuario y el correo electronico para que no haya datos duplicados en la tabla de PROFILE y ACCOUNT.
                cursor.execute(
                    "SELECT * FROM PROFILE WHERE nickname_profile = %s", (username,))
                username_encontrado = cursor.fetchone()
                cursor.execute(
                    "SELECT * FROM ACCOUNT WHERE email_account = %s", (email,))
                email_encontrado = cursor.fetchone()

                # Si se encuentra un correo electronico y/o un nombre de usuario en la base de datos no se permitira registrarse, debe ingresarse un dato diferente no existente.
                if username_encontrado:
                    print("EL NOMBRE DE USUARIO INGRESADO YA ESTA EN USO")
                    return "EL NOMBRE DE USUARIO INGRESADO YA ESTA EN USO"
                if email_encontrado:
                    print("EL CORREO ELECTRÓNICO INGRESADO YA ESTA EN USO")
                    return "EL CORREO ELECTRÓNICO INGRESADO YA ESTA EN USO"
                else:  # Si nada esta duplicado se procede con la insersion de datos a la base de datos.
                    cursor.execute(
                        # Se inserta en la tabla ACCOUNT el correo electronico y contraseña.
                        "INSERT INTO ACCOUNT (email_account, pass_account, document_account) VALUES (%s, %s, %s)", (email, password, document))
                    if biography:
                        # Dependiendo de que si o no se ingrese datos de biografia, si se deben ingresaran los datos a la tabla PROFILE, el nombre de usuario y ruta por defecto de la  imagen de perfil.
                        cursor.execute(
                            "INSERT INTO PROFILE (nickname_profile, biography_profile, image_profile) VALUES (%s, %s, %s)", (username, biography, imageProfile,))
                    else:
                        cursor.execute(
                            "INSERT INTO PROFILE (nickname_profile, biography_profile, image_profile) VALUES (%s, %s, %s)", (username, '', imageProfile))
                    # Confirmar los cambios en la base de datos y redirigir a la ruta inicio.
                    mydb.commit()
                    return redirect(url_for('login'))

            else:
                print("MIEMBRO NO ENCONTRADO")
                return "MIEMBRO NO ENCONTRADO"
        else:
            print("DATOS NO INGRESADOS")
            return "DATOS NO INGRESADOS"
"""
# -----------------------------------------------------------------------------------------------------------

# Ruta para el procesamiento del login


@app.route('/logining', methods=['POST'])
def logining():
    if request.method == 'POST':
        # Se obtienen los datos de los inputs del formulario de login.html.
        document = int(request.form['inputDocumentNumber'])
        password = request.form['inputPass']

        if document:
            # Se verifica si el documento en la tabla MIEMBRO tiene una matricula.
            cursor.execute(
                "SELECT numeroMatricula_miembro FROM MIEMBRO WHERE numeroDocumento_miembro = %s ", (
                    document,)
            )
            #Si se encuentra una mtricula, se almacenará en miembro_encontrado.
            miembro_encontrado = cursor.fetchone()
            
            if miembro_encontrado:
                #Al encontrarse la matricula, se procede a verificar la contraseña ingresada.
                cursor.execute(
                    "SELECT * FROM MIEMBRO WHERE numeroDocumento_miembro = %s", (password,)
                )
                contraseña_verificada = cursor.fetchone()
                #Si la contraseña ingresada se verifica el miembro ya estara logueado.
                if contraseña_verificada:
                    #Se guarda una session con el valor de la matricula del miembro.
                    session['miembroLogueado'] = miembro_encontrado
                    # Si la contraseña es verificada se redireccionará a la ruta inicio.
                    return redirect(url_for('inicio'))
                else:
                    print("CONTRASEÑA INCORRECTA")
                    return "CONTRASEÑA INCORRECTA"
            else:
                print("MIEMBRO NO ENCONTRADO")
                return "MIEMBRO NO ENCONTRADO"
        else:
            print("DATOS NO INGRESADOS")
            return "DATOS NO INGRESADOS"
# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de perfil.


@app.route('/perfil')
def perfil():
    if "miembroLogueado" in session:  # Aqui se verifica si la session de miembro esta abierta y si no la hay no se podra acceder al perfil.
        #A esta variable se comparte el valor de la matricula de la session del miembro logueado.
        miembroLogueado = int(session['miembroLogueado'][0])
        print("EL TIPO DE ARCHIVO ES: ", type(miembroLogueado), miembroLogueado)
        #Se consulta el nombre, apellido, tipo, grado y grupo del miembro de acuerdo a su matricula.
        cursor.execute("SELECT nombre_miembro, apellido_miembro, tipo_miembro, grado_miembro, grupo_miembro FROM MIEMBRO WHERE numeroMatricula_miembro = %s", (miembroLogueado,))
        datosMiembro = cursor.fetchone()
        if datosMiembro:
            # Separar por variable como texto los datos arrojados por la consulta.
            nombre = str(datosMiembro[0])
            apellido = str(datosMiembro[1])
            tipo = str(datosMiembro[2])
            grado = str(datosMiembro[3])
            grupo = str(datosMiembro[4])
        
        # Aqui se renderiza perfil.html y se carga los datos anteriormente separados encontrados en la consulta.
        return render_template('perfil.html', nombre=nombre, apellido=apellido, tipo=tipo, grado=grado, grupo=grupo)
    else:
        # Aqui se redirecciona a login, ya que no hay una session abierta.
        return redirect(url_for('login'))
# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de manejo de los miembros


@app.route('/miembros')
def miembros():
    #Aqui se toman los datos que estan guardados en la base de datos para mostrarlos en "miembros.html"
    cursor.execute('SELECT * FROM MIEMBRO')
    miembros_registrados = cursor.fetchall()
    # Reemplazar los valores None por un espacio en blanco en los resultados
    miembros_registrados_con_blancos = [tuple('' if valor is None else valor for valor in miembro) for miembro in miembros_registrados]
    #Conteo de cuantos estudiantes hay registrados
    cursor.execute('SELECT COUNT(tipo_miembro) FROM MIEMBRO WHERE tipo_miembro= "Estudiante"')
    total_estudiantes= cursor.fetchone()
    #Conteo de cuantos profesores hay registrados
    cursor.execute('SELECT COUNT(tipo_miembro) FROM MIEMBRO WHERE tipo_miembro= "Profesor"')
    total_profesores= cursor.fetchone()
    return render_template('miembros.html',miembros= tuple(list(reversed(miembros_registrados_con_blancos))), total_estudiantes= total_estudiantes, total_profesores= total_profesores)

#Ruta para insertar datos a miembros

@app.route('/miembros/insertar', methods= ['GET','POST'])
def insertarmiembro():
    if request.method == 'POST':

        #Captura de los datos puestos en el formulario 

        matricula= request.form['numero_matricula']
        documento= request.form['numero_documento']
        nombre= request.form['nombre']
        apellido= request.form['apellido']
        tipo_miembro = request.form['tipo_miembro']
        grado= request.form['grado']
        grupo= request.form['grupo']

        #si el tipo de miebro es Profesor los campos grado y grupo pasan a ser nulos, ya que un porfesor no pertenece a un grado o a un grupo
        if tipo_miembro == 'Profesor':
            grado = None
            grupo = None

        try:
            #Se hace la peticion de Mysql para insertar los datos
            cursor.execute('INSERT INTO MIEMBRO (numeroMatricula_miembro,nombre_miembro,apellido_miembro,numeroDocumento_miembro,tipo_miembro,grado_miembro,grupo_miembro) VALUES (%s,%s,%s,%s,%s,%s,%s)',(matricula,nombre,apellido,documento,tipo_miembro,grado,grupo,))
            #se suben los cambios hechos a la base de datos
            mydb.commit()
            #Mensaje para mostrar en el estatus de la interfaz de miembros
            flash('Datos del miembro guardados correctamente.')
            return redirect(url_for('miembros'))
        except Exception:
            if tipo_miembro == 'Estudiante':
                #Si el tipo de miembro es estudiante, los campos grado y grupo deben ser seleccionados, sino hace la siguiente funcion
                if grado == '#' and grupo == '#' and grado == '#' or grupo == '#':
                    flash('Error, los campos grado y grupo deben ser seleccionados para estudiante, no pueden estar en "#" '  )
                    return redirect(url_for('miembros'))
            if tipo_miembro == '#':
                flash ('Seleccione el tipo de miembro.')
                return redirect(url_for('miembros'))

            #si ocurre un error, se mostrara este mensaje
            if Exception:
                flash(f'Fallo en guardar los datos, intente de nuevo. {Exception}')
                return redirect(url_for('miembros'))
    return render_template('insert.html')

#Ruta para eliminar miembros

@app.route('/miembros/eliminar/<string:id_miembro>')
def eliminar_miembro(id_miembro):
    #consulta para eliminar el miembro de la base de datos
    cursor.execute('DELETE  FROM MIEMBRO WHERE id_miembro = %s',(id_miembro,))
    #Subir los cambios realizados a la base de datos
    mydb.commit()
    flash ('Miembro Eliminado Correctamente')
    return redirect(url_for('miembros'))

@app.route('/miembros/refresh')
def miembros_refresh():
    try:
        miembros()
        mydb.commit()
        flash('Datos recargados correctamente')
        return redirect(url_for('miembros'))
    except Exception:
        flash(f'Error al cargar los datos, {Exception}')
        return redirect(url_for('miembros'))
    
# Ruta para editar miembro
@app.route('/miembros/editar/<string:id_miembro>', methods= ['GET','POST'])
def editar_miembro(id_miembro):
    cursor.execute('SELECT * FROM MIEMBRO WHERE id_miembro = %s',(id_miembro,))
    datos = cursor.fetchall()
    if request.method == 'POST':
        #Captura de los datos puestos en el formulario 

        matricula= request.form['numero_matricula']
        documento= request.form['numero_documento']
        nombre= request.form['nombre']
        apellido= request.form['apellido']
        tipo_miembro = request.form['tipo_miembro']
        grado= request.form['grado']
        grupo= request.form['grupo']
        try:
            cursor.execute('UPDATE MIEMBRO SET numeroMatricula_miembro = %s, nombre_miembro = %s, apellido_miembro = %s, numeroDocumento_miembro = %s, tipo_miembro = %s, grado_miembro = %s, grupo_miembro = %s WHERE id_miembro = %s',(matricula,nombre,apellido,documento,tipo_miembro,grado,grupo, id_miembro ,  ))
            mydb.commit()
            flash('Miembro actualizado correctamente')
            return redirect(url_for('miembros'))
        except :
            flash('Error.')
            return redirect(url_for('miembros'))

    return render_template('editar_miembro.html', id_miembro=id_miembro, datos_miembro=datos)
# -----------------------------------------------------------------------------------------------------------
# AUN SIN TERMINAR********


@app.route('/grupos')
def grupos():
    if 'miembroLogueado' in session:
        cursor.execute("SELECT * FROM GRUPO")
        grupos_registrados = cursor.fetchall()
        grupos_spacesWhite = [tuple(
            '' if valor is None else valor for valor in grupo) for grupo in grupos_registrados]
        return render_template('grupos.html', grupos=tuple(list(reversed(grupos_spacesWhite))))
    else:
        return redirect(url_for('login'))


@app.route('/grupos/search', methods=['GET', 'POST'])
def search_group():
    if request.method == 'POST':
        nombreGrupo = request.form['grupo_aBuscar']
        if nombreGrupo.strip():
            cursor.execute(
                "SELECT * FROM GRUPO WHERE nombre_grupo LIKE %s ESCAPE '\\'", (f'{nombreGrupo.strip()}%',))
            grupos_encontrados = cursor.fetchall()
            grupos_spacesWhite = [tuple(
                                  '' if valor is None else valor for valor in grupo) for grupo in grupos_encontrados]
            return render_template('grupos.html', grupos=tuple(list(reversed(grupos_spacesWhite))))
        else:

            return redirect(url_for('grupos'))


# -----------------------------------------------------------------------------------------------------------
# Funcion para cerrar sesión


@app.route('/logout')
def logout():
    # Aqui se elimina mediante ".pop" y si no hay una session devolverá "None".
    session.pop('miembroLogueado', None)
    # Finalmente se redirecciona a la pantalla de login.
    return redirect(url_for('login'))
# -----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True, port=4000)
