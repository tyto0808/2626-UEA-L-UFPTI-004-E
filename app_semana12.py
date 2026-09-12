```python
import mysql.connector

from flask import Flask, render_template, redirect, url_for

from forms.especie_form import EspecieForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS MYSQL
# ============================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",
        database="proyecto_integrador"
    )


# ============================================================
# CONFIGURACIÓN DE FLASK
# ============================================================

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave-secreta-semana-13'


# ============================================================
# ALMACENAMIENTO TEMPORAL
# ============================================================
# Estos módulos todavía utilizan almacenamiento temporal.
# Productos utiliza MySQL.

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
# PRODUCTOS - MYSQL
# ============================================================

@app.route('/productos', methods=['GET', 'POST'])
def productos():

    form = ProductoForm()

    # --------------------------------------------------------
    # INSERT - AGREGAR PRODUCTO EN MYSQL
    # --------------------------------------------------------

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO productos
            (nombre, categoria, precio, cantidad)
            VALUES (%s, %s, %s, %s)
            ''',
            (
                form.nombre.data,
                form.categoria.data,
                float(form.precio.data),
                form.cantidad.data
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('productos'))

    # --------------------------------------------------------
    # SELECT - LISTAR PRODUCTOS
    # --------------------------------------------------------

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT id, nombre, categoria, precio, cantidad
        FROM productos
        ORDER BY id DESC
        '''
    )

    productos_db = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'productos.html',
        form=form,
        productos=productos_db
    )


# ============================================================
# MODIFICAR PRODUCTO
# ============================================================

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar producto
    cursor.execute(
        '''
        SELECT id, nombre, categoria, precio, cantidad
        FROM productos
        WHERE id = %s
        ''',
        (id,)
    )

    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if producto is None:
        return redirect(url_for('productos'))

    form = ProductoForm()

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            '''
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                cantidad = %s
            WHERE id = %s
            ''',
            (
                form.nombre.data,
                form.categoria.data,
                float(form.precio.data),
                form.cantidad.data,
                id
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('productos'))

    # Cargar los datos actuales en el formulario
    if not form.is_submitted():
        form.nombre.data = producto['nombre']
        form.categoria.data = producto['categoria']
        form.precio.data = producto['precio']
        form.cantidad.data = producto['cantidad']

    return render_template(
        'editar_producto.html',
        form=form,
        producto=producto
    )


# ============================================================
# ELIMINAR PRODUCTO
# ============================================================

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        DELETE FROM productos
        WHERE id = %s
        ''',
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('productos'))


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
```
