# Autor Jose Galarza
from flask import Flask, redirect, url_for
from libros_autores import libros_autores
from usuarios import usuarios

app = Flask(__name__)
app.register_blueprint(libros_autores)
app.register_blueprint(usuarios)

@app.route('/')
def index():
    return redirect(url_for('libros_autores.admi_autores'))


if __name__ == "__main__":
    app.run(debug=True, port=5005)