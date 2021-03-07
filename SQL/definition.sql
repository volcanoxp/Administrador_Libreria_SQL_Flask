-- # Autor Jose Galarza
--Name DATABASE: Libreria_Flask

CREATE DATABASE Libreria_Flask

USE Libreria_Flask

CREATE TABLE autores(
    autor_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    apellido VARCHAR(30) NOT NULL,
    seudonimo VARCHAR(30) NOT NULL,
    genero ENUM('M','F'),
    pais_origen VARCHAR(30) NOT NULL,
    fecha_creacion DATETIME DEFAULT current_timestamp
);

CREATE TABLE libros(
    libro_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    autor_id INT UNSIGNED NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion VARCHAR(50) NOT NULL,
    fecha_publicacion DATE NOT NULL,
    ventas INT UNSIGNED NOT NULL,
    stock INT UNSIGNED NOT NULL, 
    FOREIGN KEY (autor_id) REFERENCES autores(autor_id)
);

CREATE TABLE usuarios(
    usuario_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    apellido VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    fecha_creacion DATETIME DEFAULT current_timestamp
);

CREATE TABLE prestamos_usuarios(
    usuario_id INTEGER UNSIGNED NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    username VARCHAR(39) NOT NULL,
    total_prestamos INT UNSIGNED NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

CREATE TABLE libros_usuario(
    libro_id INT UNSIGNED NOT NULL,
    usuario_id INT UNSIGNED NOT NULL,
    
    FOREIGN KEY (libro_id) REFERENCES libros(libro_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    fecha_creacion DATETIME DEFAULT current_timestamp
);


-- CREACION DE LOS PROCEDIMIENTOS
DELIMITER //
CREATE PROCEDURE prestamo(libro_id INT, usuario_id INT)
BEGIN
    SET @cantidad = (SELECT stock FROM libros WHERE libros.libro_id = libro_id);
    
    IF @cantidad > 0 THEN
        INSERT INTO libros_usuario(libro_id,usuario_id) VALUES (libro_id,usuario_id);
        UPDATE libros SET stock = stock -1 WHERE libros.libro_id = libro_id;

        SET @exist = (SELECT COUNT(*) FROM prestamos_usuarios WHERE prestamos_usuarios.usuario_id = usuario_id);

        IF @exist = 0 THEN
            SET @nombre = (SELECT nombre FROM usuarios WHERE usuarios.usuario_id = usuario_id);
            SET @email = (SELECT email FROM usuarios WHERE usuarios.usuario_id = usuario_id);
            SET @username = (SELECT username FROM usuarios WHERE usuarios.usuario_id = usuario_id);
            INSERT INTO prestamos_usuarios(usuario_id,nombre,email,username,total_prestamos) VALUES (usuario_id,@nombre,@email,@username,1);
        ELSE
            UPDATE prestamos_usuarios set total_prestamos = total_prestamos + 1 WHERE prestamos_usuarios.usuario_id = usuario_id;
        END IF;

    ELSE
        UPDATE libros SET descripcion = 'No disponible' WHERE libros.libro_id = libro_id; 
        SELECT "No es posible realizar el prestamo" AS mensaje_error;
    END IF;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE venta(libro_id INT)
BEGIN
    SET @cantidad = (SELECT stock FROM libros WHERE libros.libro_id = libro_id);

    IF @cantidad > 0 THEN
        UPDATE libros SET stock = stock - 1 WHERE libros.libro_id = libro_id;
        UPDATE libros SET ventas = ventas + 1 WHERE libros.libro_id = libro_id;
    ELSE
        UPDATE libros SET descripcion = 'No disponible' WHERE libros.libro_id = libro_id;
        SELECT "No se cuenta con stock" AS mensaje_error;
    END IF;

END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE devolucion_libro(libro_id INT, usuario_id INT) 
BEGIN 
    SET @cantidad = (SELECT stock FROM libros WHERE libros.libro_id = libro_id);

    DELETE FROM libros_usuario WHERE libros_usuario.libro_id = libro_id AND libros_usuario.usuario_id = usuario_id;
    UPDATE libros SET stock = stock + 1 WHERE libros.libro_id = libro_id;

    IF @cantidad = 0 THEN
        UPDATE libros SET descripcion = 'Disponible' WHERE libros.libro_id = libro_id;
    END IF;

END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE aumentar_stock(libro_id INT, cantidad INT)
BEGIN
    UPDATE libros SET stock = stock + cantidad WHERE libros.libro_id = libro_id;
    UPDATE libros SET descripcion = 'Disponible' WHERE libros.libro_id = libro_id;
END//
DELIMITER ;


