# Autor Jose Galarza

from flask import Blueprint, redirect, url_for, render_template, request
from database import db

usuarios = Blueprint('usuarios', __name__, static_folder='static', template_folder='templates')

@usuarios.route('/usuarios', methods=['GET','POST'])
def admin_usuarios():
    if request.method == 'GET':
        data = db.get_tabla_usuarios()
        return render_template('admin_usuarios.html',data = data)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        username = request.form['username']
        correo = request.form['correo']

        db.insert_table_usuarios(nombre,apellido,username,correo)

        return redirect(url_for('usuarios.admin_usuarios'))

@usuarios.route('/usuarios/prestamos_devoluciones',methods=['GET','POST'])
def admin_prestamos_devoluciones():
    if request.method == 'GET':
        return render_template('admin_prestamos_devoluciones.html')

    if request.method == 'POST':
        
        try:
            if (request.form['libro_id'] == ''):
                libro_id = 0
            else:
                libro_id = int(request.form['libro_id'])
            
            titulo = request.form['titulo']

            if (request.form['usuario_id'] == ''):
                usuario_id = 0
            else:
                usuario_id = int(request.form['usuario_id'])
            
            nombre = request.form['nombre']
            correo = request.form['correo']
            
            data1, data2 = db.consulta_libro_usuario(libro_id,titulo,usuario_id,nombre,correo)
            data_historial_user = db.consulta_historial_usuario(usuario_id,nombre,correo)
            data_libro_prestados = db.consulta_libros_prestados_usuario(usuario_id,nombre,correo)

            return render_template('admin_prestamos_devoluciones.html', data_libro= data1, data_user=data2, data_historial_user=data_historial_user, data_libro_prestados=data_libro_prestados)

        except:
            return redirect(url_for('usuarios.admin_prestamos_devoluciones'))

@usuarios.route('/usuarios/prestamos', methods=['POST'])
def prestamos_libro():
    if request.method == 'POST':
        try:
            libro_id=0
            if (request.form['libro_id'] != ''):
                libro_id = int(request.form['libro_id'])
                
            usuario_id=0
            if (request.form['usuario_id'] != ''):
                usuario_id = int(request.form['usuario_id'])

            db.prestamo_libro(libro_id,usuario_id)
            mensaje = "Se realizo el prestamo"

            return render_template('admin_prestamos_devoluciones.html', mensaje_prestamo=mensaje)
        except:
            return redirect(url_for('usuarios.admin_prestamos_devoluciones'))

@usuarios.route('/usuarios/devolucion', methods=['POST'])
def devolucion_libro():
    if request.method == 'POST':
        try:
            libro_id=0
            if (request.form['libro_id'] != ''):
                libro_id = int(request.form['libro_id'])

            usuario_id=0
            if (request.form['usuario_id'] != ''):
                usuario_id = int(request.form['usuario_id'])

            db.devolucion_libro(libro_id,usuario_id)
            mensaje = "Se realizo la devolucion"

            return render_template('admin_prestamos_devoluciones.html', mensaje_devolucion=mensaje)
        except:
            return redirect(url_for('usuarios.admin_prestamos_devoluciones'))

@usuarios.route('/usuarios/historial_usuario')
def historial_usuarios():
    data_historial_user = db.consulta_historial_usuario_total()
    return render_template('historial_usuarios.html',data_historial_user=data_historial_user)

@usuarios.route('/usuarios/historial_usuario_libros')
def historial_libros_usuarios():
    data_libro_prestados = db.consulta_libros_prestados_usuario_total()
    return render_template('historial_libros_prestados.html',data_libro_prestados=data_libro_prestados)


