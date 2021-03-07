# Autor Jose Galarza

import MySQLdb

class database():

    def __init__(self):
        self.__host = 'localhost'
        self.__user = 'root'
        self.__passw = ''
        self.__db = 'Libreria_Flask'
        self.mysql = MySQLdb.connect(host=self.__host, user=self.__user, passwd=self.__passw,db=self.__db)

    def insert_table_autores(self,nombre,apellido,seudonimo,genero,pais):
        self.mysql.query(F"""
        INSERT INTO autores(nombre,apellido,seudonimo,genero,pais_origen)
        VALUES ('{nombre}', '{apellido}', '{seudonimo}', '{genero}', '{pais}')
        """)
        self.mysql.commit()

    def insert_table_libros(self,autor_id,titulo,descripcion,fecha_publicacion,ventas,stock):
        self.mysql.query(f"""
        INSERT INTO libros(autor_id,titulo,descripcion,fecha_publicacion,ventas,stock)
        VALUES ({autor_id},'{titulo}','{descripcion}','{fecha_publicacion}',{ventas},{stock})
        """)
        self.mysql.commit()

    def insert_table_usuarios(self, nombre, apellido, username, email):
        self.mysql.query(f"""
        INSERT INTO usuarios(nombre,apellido,username,email)
        VALUES ('{nombre}', '{apellido}', '{username}', '{email}')
        """)
        self.mysql.commit()

    def prestamo_libro(self, libro_id, usuario_id):
        self.mysql.query(f"""
        CALL prestamo({libro_id},{usuario_id})
        """)
        self.mysql.commit()
    
    def venta_libro(self, libro_id):
        self.mysql.query(f"""
        CALL venta({libro_id})
        """)
        self.mysql.commit()

    def devolucion_libro(self, libro_id, usuario_id):
        self.mysql.query(f"""
        CALL devolucion_libro({libro_id},{usuario_id})
        """)
        self.mysql.commit()

    def aumentar_stock(self, libro_id, cantidad):
        self.mysql.query(f"""
        CALL aumentar_stock({libro_id},{cantidad})
        """)
        self.mysql.commit()

    def get_table_autores(self):
        self.mysql.query("""
        SELECT * FROM autores
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data

    def get_table_libros(self):
        self.mysql.query("""
        SELECT * FROM libros
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data

    def get_autor_id(self,nombre,apellido):
        self.mysql.query(f"""
        SELECT autor_id,nombre, apellido FROM autores
        WHERE autores.nombre = '{nombre}' OR autores.apellido = '{apellido}'
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data

    def get_tabla_usuarios(self):
        self.mysql.query("""
        SELECT * FROM usuarios
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data

    def consulta_libro_usuario(self, libro_id, titulo,usuario_id,nombre, correo):
        self.mysql.query(f"""
        SELECT libro_id, titulo, CONCAT(autores.nombre,' ',autores.apellido) AS autor FROM libros
        INNER JOIN autores ON autores.autor_id = libros.autor_id
        WHERE libros.libro_id = {libro_id} OR libros.titulo = '{titulo}'
        """)
        data1 = self.mysql.store_result().fetch_row(maxrows=0)

        self.mysql.query(f"""
        SELECT usuario_id, nombre, apellido, email FROM usuarios
        WHERE usuarios.usuario_id = {usuario_id} OR usuarios.nombre = '{nombre}' OR usuarios.email = '{correo}'
        """)
        data2 = self.mysql.store_result().fetch_row(maxrows=0)

        return data1, data2

    def consulta_historial_usuario(self, usuario_id, nombre, correo):
        self.mysql.query(f"""
        SELECT usuario_id, nombre, email, total_prestamos FROM prestamos_usuarios
        WHERE prestamos_usuarios.usuario_id = {usuario_id} OR prestamos_usuarios.nombre = '{nombre}'
                OR prestamos_usuarios.email = '{correo}'
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data

    def consulta_historial_usuario_total(self):
        self.mysql.query(f"""
        SELECT usuario_id, nombre, email, total_prestamos FROM prestamos_usuarios
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data


    def consulta_libros_prestados_usuario(self, usuario_id, nombre, correo):
        self.mysql.query(f"""
        SELECT libros.libro_id, usuarios.usuario_id, nombre, apellido, titulo
        FROM libros_usuario
        INNER JOIN usuarios ON usuarios.usuario_id = libros_usuario.usuario_id
        INNER JOIN libros ON libros.libro_id = libros_usuario.libro_id
        WHERE usuarios.usuario_id = {usuario_id} OR usuarios.nombre = '{nombre}'
                OR usuarios.email = '{correo}'
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data

    def consulta_libros_prestados_usuario_total(self):
        self.mysql.query(f"""
        SELECT libros.libro_id, usuarios.usuario_id, nombre, apellido, titulo
        FROM libros_usuario
        INNER JOIN usuarios ON usuarios.usuario_id = libros_usuario.usuario_id
        INNER JOIN libros ON libros.libro_id = libros_usuario.libro_id
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data

    def consulta_libro(self, libro_id, titulo):
        self.mysql.query(f"""
        SELECT libro_id, titulo, CONCAT(autores.nombre,' ', autores.apellido) AS autor, stock FROM libros
        INNER JOIN autores ON autores.autor_id = libros.autor_id
        WHERE libros.libro_id = {libro_id} OR libros.titulo = '{titulo}'
        """)
        data = self.mysql.store_result().fetch_row(maxrows=0)
        return data

db = database()
