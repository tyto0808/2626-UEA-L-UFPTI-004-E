const formulario = document.getElementById("formRegistro");

const nombre = document.getElementById("nombre");
const categoria = document.getElementById("categoria");
const descripcion = document.getElementById("descripcion");

const errorNombre = document.getElementById("errorNombre");
const errorCategoria = document.getElementById("errorCategoria");
const errorDescripcion = document.getElementById("errorDescripcion");

const mensajeGeneral = document.getElementById("mensajeGeneral");
const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");

const botonAgregar = document.getElementById("btnAgregar");
const textoBoton = document.getElementById("textoBoton");
const spinnerRegistro = document.getElementById("spinnerRegistro");

const modalNombre = document.getElementById("modalNombre");
const modalCategoria = document.getElementById("modalCategoria");
const modalDescripcion = document.getElementById("modalDescripcion");

let contador = 0;

/* VALIDACIÓN DEL NOMBRE */
function validarNombre() {
    const valorNombre = nombre.value.trim();

    if (valorNombre === "") {
        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.textContent =
            "El nombre de la especie es obligatorio.";

        return false;
    }

    if (valorNombre.length < 3) {
        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.textContent =
            "El nombre debe tener mínimo 3 caracteres.";

        return false;
    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");
    errorNombre.textContent = "";

    return true;
}

/* VALIDACIÓN DE LA CATEGORÍA */
function validarCategoria() {
    if (categoria.value === "") {
        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        errorCategoria.textContent =
            "Debe seleccionar una categoría.";

        return false;
    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");
    errorCategoria.textContent = "";

    return true;
}

/* VALIDACIÓN DE LA DESCRIPCIÓN */
function validarDescripcion() {
    const valorDescripcion = descripcion.value.trim();

    if (valorDescripcion === "") {
        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.textContent =
            "La descripción es obligatoria.";

        return false;
    }

    if (valorDescripcion.length < 10) {
        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.textContent =
            "La descripción debe tener mínimo 10 caracteres.";

        return false;
    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");
    errorDescripcion.textContent = "";

    return true;
}

/* MOSTRAR ALERTAS DE BOOTSTRAP */
function mostrarMensaje(texto, tipo) {
    mensajeGeneral.innerHTML = "";

    const alerta = document.createElement("div");

    alerta.className = `alert ${tipo} alert-dismissible fade show`;
    alerta.setAttribute("role", "alert");

    alerta.textContent = texto;

    const botonCerrar = document.createElement("button");

    botonCerrar.type = "button";
    botonCerrar.className = "btn-close";
    botonCerrar.setAttribute("data-bs-dismiss", "alert");
    botonCerrar.setAttribute("aria-label", "Cerrar");

    alerta.appendChild(botonCerrar);
    mensajeGeneral.appendChild(alerta);
}

/* LIMPIAR EL FORMULARIO */
function limpiarFormulario() {
    formulario.reset();

    nombre.classList.remove("is-valid", "is-invalid");
    categoria.classList.remove("is-valid", "is-invalid");
    descripcion.classList.remove("is-valid", "is-invalid");

    errorNombre.textContent = "";
    errorCategoria.textContent = "";
    errorDescripcion.textContent = "";
}

/* MOSTRAR Y OCULTAR EL SPINNER */
function activarSpinner() {
    botonAgregar.disabled = true;
    textoBoton.textContent = "Procesando...";
    spinnerRegistro.classList.remove("d-none");
}

function desactivarSpinner() {
    botonAgregar.disabled = false;
    textoBoton.textContent = "Agregar Registro";
    spinnerRegistro.classList.add("d-none");
}

/* ABRIR EL MODAL CON LOS DETALLES */
function mostrarDetalles(nombreTexto, categoriaTexto, descripcionTexto) {
    modalNombre.textContent = nombreTexto;
    modalCategoria.textContent = categoriaTexto;
    modalDescripcion.textContent = descripcionTexto;

    const modalDetalles = new bootstrap.Modal(
        document.getElementById("modalDetalles")
    );

    modalDetalles.show();
}

/* CREAR UN REGISTRO DINÁMICO */
function crearRegistro(nombreTexto, categoriaTexto, descripcionTexto) {
    const columna = document.createElement("div");
    columna.className = "col-12 col-md-6 col-lg-4 mb-4";

    const tarjeta = document.createElement("div");
    tarjeta.className = "card shadow h-100";

    const cuerpoTarjeta = document.createElement("div");
    cuerpoTarjeta.className = "card-body d-flex flex-column";

    const titulo = document.createElement("h5");
    titulo.className = "card-title text-success";
    titulo.textContent = nombreTexto;

    const tipo = document.createElement("p");
    tipo.className = "card-text";
    tipo.innerHTML =
        "<strong>Categoría:</strong> " + categoriaTexto;

    const texto = document.createElement("p");
    texto.className = "card-text";
    texto.textContent = descripcionTexto;

    const contenedorBotones = document.createElement("div");
    contenedorBotones.className =
        "mt-auto d-flex gap-2 flex-wrap";

    const botonDetalles = document.createElement("button");
    botonDetalles.type = "button";
    botonDetalles.textContent = "Ver detalles";
    botonDetalles.className = "btn btn-primary";

    botonDetalles.addEventListener("click", function () {
        mostrarDetalles(
            nombreTexto,
            categoriaTexto,
            descripcionTexto
        );
    });

    const botonEliminar = document.createElement("button");
    botonEliminar.type = "button";
    botonEliminar.textContent = "Eliminar";
    botonEliminar.className = "btn btn-danger";

    botonEliminar.addEventListener("click", function () {
        const confirmar = window.confirm(
            "¿Está seguro de que desea eliminar este registro?"
        );

        if (confirmar) {
            columna.remove();

            contador--;
            total.textContent = contador;

            mostrarMensaje(
                "Registro eliminado correctamente.",
                "alert-warning"
            );
        }
    });

    contenedorBotones.appendChild(botonDetalles);
    contenedorBotones.appendChild(botonEliminar);

    cuerpoTarjeta.appendChild(titulo);
    cuerpoTarjeta.appendChild(tipo);
    cuerpoTarjeta.appendChild(texto);
    cuerpoTarjeta.appendChild(contenedorBotones);

    tarjeta.appendChild(cuerpoTarjeta);
    columna.appendChild(tarjeta);
    lista.appendChild(columna);

    contador++;
    total.textContent = contador;
}

/* VALIDACIONES EN TIEMPO REAL */
nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

/* ENVÍO DEL FORMULARIO */
formulario.addEventListener("submit", function (evento) {
    evento.preventDefault();

    const nombreValido = validarNombre();
    const categoriaValida = validarCategoria();
    const descripcionValida = validarDescripcion();

    if (!nombreValido || !categoriaValida || !descripcionValida) {
        mostrarMensaje(
            "Corrija los errores antes de registrar la información.",
            "alert-danger"
        );

        return;
    }

    activarSpinner();

    const nombreRegistro = nombre.value.trim();
    const categoriaRegistro = categoria.value;
    const descripcionRegistro = descripcion.value.trim();

    setTimeout(function () {
        crearRegistro(
            nombreRegistro,
            categoriaRegistro,
            descripcionRegistro
        );

        mostrarMensaje(
            "Registro agregado correctamente.",
            "alert-success"
        );

        limpiarFormulario();
        desactivarSpinner();
    }, 1500);
});