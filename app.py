from flask import Flask, render_template, redirect, url_for

from forms.especie_form import EspecieForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

# SECRET_KEY necesaria para Flask-WTF y protección CSRF
app.config['SECRET_KEY'] = 'clave-secreta-semana-11'


# ============================================================
# ALMACENAMIENTO TEMPORAL
# ============================================================

especies_registradas = []
productos_registrados = []
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
# PRODUCTOS
# ============================================================

@app.route('/productos', methods=['GET', 'POST'])
def productos():

    form = ProductoForm()

    if form.validate_on_submit():

        nuevo_producto = {
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
            'precio': form.precio.data,
            'cantidad': form.cantidad.data
        }

        productos_registrados.append(nuevo_producto)

        return redirect(url_for('productos'))

    return render_template(
        'productos.html',
        form=form,
        productos=productos_registrados
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