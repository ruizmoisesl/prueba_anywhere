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
    host='localhost',
    user='root',
    database='indenetwork'
)

# Ejecutador de comandos/consultas de la base de datos.
cursor = mydb.cursor()
# ------------------------------------------------------------------------------------------------------------

# Ruta de la pagina principal.


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/miembros')
def miembros():
    #Aqui se toman los datos que estan guardados en la base de datos para mostrarlos en "miembros.html"
    cursor.execute('SELECT * FROM MIEMBROS')
    miembros_registrados = cursor.fetchall()
    # Reemplazar los valores None por un espacio en blanco en los resultados
    miembros_registrados_con_blancos = [tuple('' if valor is None else valor for valor in miembro) for miembro in miembros_registrados]
    #Conteo de cuantos estudiantes hay registrados
    cursor.execute('SELECT COUNT(tipo_miembro) FROM MIEMBROS WHERE tipo_miembro= "Estudiante"')
    total_estudiantes= cursor.fetchone()
    #Conteo de cuantos profesores hay registrados
    cursor.execute('SELECT COUNT(tipo_miembro) FROM MIEMBROS WHERE tipo_miembro= "Profesor"')
    total_profesores= cursor.fetchone()
    return render_template('miembros.html',miembros= tuple(list(reversed(miembros_registrados_con_blancos))), total_estudiantes= total_estudiantes, total_profesores= total_profesores)

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
            cursor.execute('INSERT INTO MIEMBROS (matricula,nombre,apellido,documento,tipo_miembro,grado,grupo) VALUES (%s,%s,%s,%s,%s,%s,%s)',(matricula,nombre,apellido,documento,tipo_miembro,grado,grupo,))
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


@app.route('/miembros/eliminar/<string:id_miembro>')
def eliminar_miembro(id_miembro):
    cursor.execute('DELETE  FROM MIEMBROS WHERE id_miembro = %s',(id_miembro,))
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
    
@app.route('/miembros/editar/<string:id_miembro>', methods= ['GET','POST'])
def editar_miembro(id_miembro):
    cursor.execute('SELECT * FROM MIEMBROS WHERE id_miembro = %s',(id_miembro,))
    datos = cursor.fetchall()
    if request.method == 'POST':
        matricula= request.form['numero_matricula']
        documento= request.form['numero_documento']
        nombre= request.form['nombre']
        apellido= request.form['apellido']
        tipo_miembro = request.form['tipo_miembro']
        grado= request.form['grado']
        grupo= request.form['grupo']
        try:
            cursor.execute('UPDATE MIEMBROS SET numeroMatricula_miembro = %s, nombre_miembro = %s, apellido_miembro = %s, numeroDocumento_miembro = %s, tipo_miembro = %s, grado_miembro = %s, grupo_miembro = %s WHERE id_miembro = %s',(matricula,nombre,apellido,documento,tipo_miembro,grado,grupo, id_miembro ,  ))
            mydb.commit()
            flash('Miembro actualizado correctamente')
            return redirect(url_for('miembros'))
        except :
            flash('Error.')
            return redirect(url_for('miembros'))

    return render_template('editar_miembro.html', id_miembro=id_miembro, datos_miembro=datos)



if __name__ == '__main__':
    app.run(debug=True, port=4000)
