# Autor Jose Galarza

from flask import Blueprint,request , redirect, render_template, url_for
from database import db

libros_autores = Blueprint('libros_autores',__name__,static_folder='static', template_folder='templates')

@libros_autores.route('/autores', methods=['GET','POST'])
def admi_autores():
    if request.method == 'GET':
        data = db.get_table_autores()
        
        return render_template('admin_autores.html', data=data)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        seudonimo = request.form['seudonimo']
        genero = request.form['genero']
        pais = request.form['pais']

        db.insert_table_autores(nombre,apellido,seudonimo,genero,pais)

        return redirect(url_for('libros_autores.admi_autores'))

@libros_autores.route('/libros', methods=['GET','POST'])
def admin_libros():
    if request.method == 'GET':
        data = db.get_table_libros()
        return render_template('admin_libros.html', data=data)

    if request.method == 'POST':
        autor_id = request.form['autor_id']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_publicacion = request.form['fecha_publicacion']
        ventas = request.form['ventas']
        stock = request.form['stock']
        
        db.insert_table_libros(autor_id,titulo,descripcion,fecha_publicacion,ventas,stock)

        return redirect(url_for('libros_autores.admin_libros'))

@libros_autores.route('/buscar_autor_id', methods=['POST'])
def buscar_autor_id():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        
        data_autor = db.get_autor_id(nombre,apellido)

        data = db.get_table_libros()
        return render_template('admin_libros.html', data=data, data_autor = data_autor)


@libros_autores.route('/libros/aumentar_vender', methods=['GET','POST'])
def pagina_aumentar_vender():
    if request.method == 'GET':
        return render_template('admin_libros_aumentar_vender.html')

    if request.method == 'POST':
        libro_id = 0
        if (request.form['libro_id'] != ''):
            libro_id = int(request.form['libro_id'])
        titulo = request.form['titulo']
        consulta_libro = db.consulta_libro(libro_id,titulo)
        return render_template('admin_libros_aumentar_vender.html',consulta_libro=consulta_libro)

@libros_autores.route('/libros/aumentar', methods=['POST'])
def libro_aumentar():
    if request.method == 'POST':
        libro_id = 0
        if (request.form['libro_id'] != ''):
            libro_id = int(request.form['libro_id'])
        cantidad = 0
        if (request.form['cantidad'] != ''):
            cantidad = int(request.form['cantidad'])

        db.aumentar_stock(libro_id,cantidad)
        mensaje_aumentar = "Se aumento con éxito"
        return render_template('admin_libros_aumentar_vender.html', mensaje_aumentar=mensaje_aumentar)

@libros_autores.route('/libros/vender', methods=['POST'])
def libro_vender():
    if request.method == 'POST':
        libro_id = 0
        if (request.form['libro_id'] != ''):
            libro_id = int(request.form['libro_id'])
        
        db.venta_libro(libro_id)
        mensaje_vender = "Se vendió el libro con éxito"
        return render_template('admin_libros_aumentar_vender.html', mensaje_vender=mensaje_vender)