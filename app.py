import os
import sqlite3

from flask import Flask, render_template, redirect, url_for

from forms.especie_form import EspecieForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS SQLITE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    'data',
    'ferreteria.db'
)


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def crear_base_datos():

    # Crear carpeta data si no existe
    os.makedirs(
        os.path.join(BASE_DIR, 'data'),
        exist_ok=True
    )

    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# ============================================================
# CONFIGURACIÓN DE FLASK
# ============================================================

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave-secreta-semana-11'


# ============================================================
# CREAR BASE DE DATOS
# ============================================================

crear_base_datos()

# Esto nos permite comprobar dónde está la base de datos
print("Base de datos utilizada:", DATABASE)


# ============================================================
# ALMACENAMIENTO TEMPORAL
# ============================================================
# Productos NO está aquí porque utiliza SQLite.

especies_registradas = []
clientes_registrados = []
proveedores_registrados = []
facturas_registradas = []


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route('/')
def home():
    return render_template('index.html')


# ============================================================
# ESPECIES / ARACNOFAUNA
# ============================================================

@app.route('/especies', methods=['GET', 'POST'])
def especies():

    form = EspecieForm()

    if form.validate_on_submit():

        nueva_especie = {
            'familia': form.familia.data,
            'genero': form.genero.data,
            'especie': form.especie.data,
            'microhabitat': form.microhabitat.data,
            'temporada': form.temporada.data,
            'tipo_monitoreo': form.tipo_monitoreo.data,
            'cantidad': form.cantidad.data,
            'observaciones': form.observaciones.data
        }

        especies_registradas.append(nueva_especie)

        return redirect(url_for('especies'))

    return render_template(
        'especies.html',
        form=form,
        especies=especies_registradas
    )


# ============================================================
# PRODUCTOS - SQLITE
# ============================================================

@app.route('/productos', methods=['GET', 'POST'])
def productos():

    form = ProductoForm()

    # --------------------------------------------------------
    # INSERT - GUARDAR EN SQLITE
    # --------------------------------------------------------

    if form.validate_on_submit():

        conn = get_db_connection()

        conn.execute(
            '''
            INSERT INTO productos
            (nombre, categoria, precio, cantidad)
            VALUES (?, ?, ?, ?)
            ''',
            (
                form.nombre.data,
                form.categoria.data,
                float(form.precio.data),
                form.cantidad.data
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for('productos'))

    # --------------------------------------------------------
    # SELECT - RECUPERAR DATOS DE SQLITE
    # --------------------------------------------------------

    conn = get_db_connection()

    productos_db = conn.execute(
        '''
        SELECT id, nombre, categoria, precio, cantidad
        FROM productos
        ORDER BY id DESC
        '''
    ).fetchall()

    conn.close()

    # --------------------------------------------------------
    # ENVIAR REGISTROS A JINJA2
    # --------------------------------------------------------

    return render_template(
        'productos.html',
        form=form,
        productos=productos_db
    )


# ============================================================
# CLIENTES
# ============================================================

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo_cliente = {
            'nombre': form.nombre.data,
            'correo': form.correo.data,
            'telefono': form.telefono.data
        }

        clientes_registrados.append(nuevo_cliente)

        return redirect(url_for('clientes'))

    return render_template(
        'clientes.html',
        form=form,
        clientes=clientes_registrados
    )


# ============================================================
# PROVEEDORES
# ============================================================

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo_proveedor = {
            'empresa': form.empresa.data,
            'contacto': form.contacto.data,
            'correo': form.correo.data,
            'telefono': form.telefono.data
        }

        proveedores_registrados.append(nuevo_proveedor)

        return redirect(url_for('proveedores'))

    return render_template(
        'proveedores.html',
        form=form,
        proveedores=proveedores_registrados
    )


# ============================================================
# FACTURACIÓN
# ============================================================

@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva_factura = {
            'cliente': form.cliente.data,
            'producto': form.producto.data,
            'cantidad': form.cantidad.data,
            'total': form.total.data
        }

        facturas_registradas.append(nueva_factura)

        return redirect(url_for('facturacion'))

    return render_template(
        'facturacion.html',
        form=form,
        facturas=facturas_registradas
    )


# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)