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

let contador = 0;

function validarNombre() {
    if (nombre.value.trim() === "") {
        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");
        errorNombre.textContent = "El nombre de la especie es obligatorio.";
        return false;
    } else if (nombre.value.trim().length < 3) {
        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");
        errorNombre.textContent = "El nombre debe tener mínimo 3 caracteres.";
        return false;
    } else {
        nombre.classList.remove("is-invalid");
        nombre.classList.add("is-valid");
        errorNombre.textContent = "";
        return true;
    }
}

function validarCategoria() {
    if (categoria.value === "") {
        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");
        errorCategoria.textContent = "Debe seleccionar una categoría.";
        return false;
    } else {
        categoria.classList.remove("is-invalid");
        categoria.classList.add("is-valid");
        errorCategoria.textContent = "";
        return true;
    }
}

function validarDescripcion() {
    if (descripcion.value.trim() === "") {
        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");
        errorDescripcion.textContent = "La descripción es obligatoria.";
        return false;
    } else if (descripcion.value.trim().length < 10) {
        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");
        errorDescripcion.textContent = "La descripción debe tener mínimo 10 caracteres.";
        return false;
    } else {
        descripcion.classList.remove("is-invalid");
        descripcion.classList.add("is-valid");
        errorDescripcion.textContent = "";
        return true;
    }
}

function mostrarMensaje(texto, tipo) {
    mensajeGeneral.innerHTML = `
        <div class="alert ${tipo}" role="alert">
            ${texto}
        </div>
    `;
}

function limpiarFormulario() {
    formulario.reset();

    nombre.classList.remove("is-valid", "is-invalid");
    categoria.classList.remove("is-valid", "is-invalid");
    descripcion.classList.remove("is-valid", "is-invalid");

    errorNombre.textContent = "";
    errorCategoria.textContent = "";
    errorDescripcion.textContent = "";
}

function crearRegistro(nombreTexto, categoriaTexto, descripcionTexto) {
    const columna = document.createElement("div");
    columna.className = "col-md-4 mb-3";

    const tarjeta = document.createElement("div");
    tarjeta.className = "card shadow p-3 h-100";

    const titulo = document.createElement("h5");
    titulo.textContent = nombreTexto;

    const tipo = document.createElement("p");
    tipo.innerHTML = "<strong>Categoría:</strong> " + categoriaTexto;

    const texto = document.createElement("p");
    texto.textContent = descripcionTexto;

    const boton = document.createElement("button");
    boton.textContent = "Eliminar";
    boton.className = "btn btn-danger";

    boton.addEventListener("click", function () {
        columna.remove();
        contador--;
        total.textContent = contador;
        mostrarMensaje("Registro eliminado correctamente.", "alert-danger");
    });

    tarjeta.appendChild(titulo);
    tarjeta.appendChild(tipo);
    tarjeta.appendChild(texto);
    tarjeta.appendChild(boton);

    columna.appendChild(tarjeta);
    lista.appendChild(columna);

    contador++;
    total.textContent = contador;
}

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

formulario.addEventListener("submit", function (e) {
    e.preventDefault();

    const nombreValido = validarNombre();
    const categoriaValida = validarCategoria();
    const descripcionValida = validarDescripcion();

    if (nombreValido && categoriaValida && descripcionValida) {
        crearRegistro(
            nombre.value.trim(),
            categoria.value,
            descripcion.value.trim()
        );

        mostrarMensaje("Registro agregado correctamente.", "alert-success");
        limpiarFormulario();
    } else {
        mostrarMensaje("Corrija los errores antes de registrar la información.", "alert-danger");
    }
});