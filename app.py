from flask import Flask, render_template

app = Flask(__name__)

# Esta es la ruta para tu página principal
@app.route('/')
def home():
    return render_template('index.html')

# Estas son las rutas para los módulos que pide tu tarea
@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')

if __name__ == '__main__':
    # Esto activará el modo de depuración para que veas los cambios al guardar
    app.run(debug=True)