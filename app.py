import os
import sqlite3
import mysql.connector

from dotenv import load_dotenv

load_dotenv()

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from forms.especie_form import EspecieForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.registro_form import RegistroForm


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# PRUEBA PARA SABER QUÉ APP.PY SE ESTÁ EJECUTANDO
# ============================================================

print("******** PRUEBA APP.PY ********")
print("ESTOY EJECUTANDO ESTE ARCHIVO:", os.path.abspath(__file__))
print("*******************************")

print("====================================")
print("CARPETA DE APP:", BASE_DIR)
print("CARPETA DE TEMPLATES:", "templates")

print(
    "BASE.HTML EXISTE:",
    os.path.exists(
        os.path.join(
            BASE_DIR,
            "templates",
            "base.html"
        )
    )
)

print(
    "INDEX.HTML EXISTE:",
    os.path.exists(
        os.path.join(
            BASE_DIR,
            "templates",
            "index.html"
        )
    )
)

print("====================================")


# ============================================================
# SQLITE - PRODUCTOS
# ============================================================

DATABASE = os.path.join(
    BASE_DIR,
    "data",
    "ferreteria.db"
)


def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def crear_base_datos():

    os.makedirs(
        os.path.join(BASE_DIR, "data"),
        exist_ok=True
    )

    conn = get_db_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
        """
    )

    conn.commit()

    conn.close()


print(
    "Base de datos utilizada:",
    DATABASE
)


# ============================================================
# MYSQL - USUARIOS
# ============================================================

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}


def get_mysql_connection():

    return mysql.connector.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"],
        port=MYSQL_CONFIG["port"]
    )


# ============================================================
# CREAR APLICACIÓN FLASK
# ============================================================

app = Flask(
    __name__,
    template_folder="templates"
)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "clave-secreta-biodiversidad"
)


# Crear base SQLite
crear_base_datos()


# ============================================================
# FLASK-LOGIN
# ============================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "acceso_restringido"


# ============================================================
# CLASE USUARIO
# ============================================================

class Usuario(UserMixin):

    def __init__(
        self,
        id,
        usuario,
        password
    ):

        self.id = id
        self.usuario = usuario
        self.password = password


# ============================================================
# CARGAR USUARIO
# ============================================================

@login_manager.user_loader
def load_user(user_id):

    conn = get_mysql_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
        """,
        (user_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()

    conn.close()

    if usuario:

        return Usuario(
            usuario["id"],
            usuario["usuario"],
            usuario["password"]
        )

    return None


# ============================================================
# PRUEBA DE CONEXIÓN MYSQL
# ============================================================

try:

    conexion = get_mysql_connection()

    print("CONEXIÓN CON MYSQL EXITOSA")

    conexion.close()

except Exception as e:

    print("ERROR DE MYSQL:", e)


# ============================================================
# LISTAS TEMPORALES
# ============================================================

especies_registradas = []

clientes_registrados = []

proveedores_registrados = []

facturas_registradas = []


# ============================================================
# INICIO
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# ACCESO RESTRINGIDO
# ============================================================

@app.route("/acceso-restringido")
def acceso_restringido():

    return render_template(
        "acceso_restringido.html"
    )


# ============================================================
# ESPECIES
# PROTEGIDO CON LOGIN
# ============================================================

@app.route(
    "/especies",
    methods=["GET", "POST"]
)
@login_required
def especies():

    form = EspecieForm()

    if form.validate_on_submit():

        especie = {
            "nombre": form.nombre.data,
            "nombre_cientifico": form.nombre_cientifico.data,
            "familia": form.familia.data
        }

        especies_registradas.append(
            especie
        )

        return redirect(
            url_for("especies")
        )

    return render_template(
        "especies.html",
        form=form,
        especies=especies_registradas
    )


# ============================================================
# PRODUCTOS
# PROTEGIDO CON LOGIN
# ============================================================

@app.route(
    "/productos",
    methods=["GET", "POST"]
)
@login_required
def productos():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO productos
            (
                nombre,
                categoria,
                precio,
                cantidad
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                form.nombre.data,
                form.categoria.data,
                float(form.precio.data),
                form.cantidad.data
            )
        )

        conn.commit()

        conn.close()

        return redirect(
            url_for("productos")
        )

    conn = get_db_connection()

    productos_db = conn.execute(
        """
        SELECT
            id,
            nombre,
            categoria,
            precio,
            cantidad
        FROM productos
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "productos.html",
        form=form,
        productos=productos_db
    )


# ============================================================
# CLIENTES
# PROTEGIDO CON LOGIN
# ============================================================

@app.route(
    "/clientes",
    methods=["GET", "POST"]
)
@login_required
def clientes():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "cedula": form.cedula.data,
            "telefono": form.telefono.data
        }

        clientes_registrados.append(
            cliente
        )

        return redirect(
            url_for("clientes")
        )

    return render_template(
        "clientes.html",
        form=form,
        clientes=clientes_registrados
    )


# ============================================================
# PROVEEDORES
# PROTEGIDO CON LOGIN
# ============================================================

@app.route(
    "/proveedores",
    methods=["GET", "POST"]
)
@login_required
def proveedores():

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor = {
            "nombre": form.nombre.data,
            "empresa": form.empresa.data,
            "telefono": form.telefono.data
        }

        proveedores_registrados.append(
            proveedor
        )

        return redirect(
            url_for("proveedores")
        )

    return render_template(
        "proveedores.html",
        form=form,
        proveedores=proveedores_registrados
    )


# ============================================================
# FACTURACIÓN
# PROTEGIDO CON LOGIN
# ============================================================

@app.route(
    "/facturacion",
    methods=["GET", "POST"]
)
@login_required
def facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        factura = {
            "cliente": form.cliente.data,
            "producto": form.producto.data,
            "cantidad": form.cantidad.data
        }

        facturas_registradas.append(
            factura
        )

        return redirect(
            url_for("facturacion")
        )

    return render_template(
        "facturacion.html",
        form=form,
        facturas=facturas_registradas
    )


# ============================================================
# REGISTRO DE USUARIOS
# ============================================================

@app.route(
    "/registro",
    methods=["GET", "POST"]
)
def registro():

    form = RegistroForm()

    if form.validate_on_submit():

        usuario = form.usuario.data

        password = form.password.data

        password_hash = generate_password_hash(
            password
        )

        try:

            conn = get_mysql_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO usuarios
                (
                    usuario,
                    password
                )
                VALUES (%s, %s)
                """,
                (
                    usuario,
                    password_hash
                )
            )

            conn.commit()

            cursor.close()

            conn.close()

            return redirect(
                url_for("login")
            )

        except mysql.connector.Error as e:

            print(
                "ERROR AL REGISTRAR:",
                e
            )

            return "El usuario ya existe o ocurrió un error."

    return render_template(
        "registro.html",
        form=form
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("home")
        )

    if request.method == "POST":

        usuario = request.form.get(
            "usuario"
        )

        password = request.form.get(
            "password"
        )

        conn = get_mysql_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                usuario,
                password
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario,)
        )

        usuario_db = cursor.fetchone()

        cursor.close()

        conn.close()

        if usuario_db:

            password_correcta = check_password_hash(
                usuario_db["password"],
                password
            )

            if password_correcta:

                usuario_obj = Usuario(
                    usuario_db["id"],
                    usuario_db["usuario"],
                    usuario_db["password"]
                )

                login_user(
                    usuario_obj
                )

                return redirect(
                    url_for("home")
                )

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos."
        )

    return render_template(
        "login.html"
    )


# ============================================================
# CERRAR SESIÓN
# ============================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )