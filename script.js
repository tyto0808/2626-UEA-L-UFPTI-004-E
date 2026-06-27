alert("Hola mundo");
alert("JavaScript funcionando");
const formulario = document.getElementById("formRegistro");
const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");

let contador = 0;

formulario.addEventListener("submit", function(e) {

    e.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const categoria = document.getElementById("categoria").value;
    const descripcion = document.getElementById("descripcion").value;

    if (nombre === "" || categoria === "" || descripcion === "") {
        alert("Todos los campos son obligatorios.");
        return;
    }

    const columna = document.createElement("div");
    columna.className = "col-md-4 mb-3";

    const tarjeta = document.createElement("div");
    tarjeta.className = "card shadow p-3";

    const titulo = document.createElement("h5");
    titulo.textContent = nombre;

    const tipo = document.createElement("p");
    tipo.innerHTML = "<strong>Categoría:</strong> " + categoria;

    const texto = document.createElement("p");
    texto.textContent = descripcion;

    const boton = document.createElement("button");
    boton.textContent = "Eliminar";
    boton.className = "btn btn-danger";

    boton.addEventListener("click", function() {
        columna.remove();
        contador--;
        total.textContent = contador;
    });

    tarjeta.appendChild(titulo);
    tarjeta.appendChild(tipo);
    tarjeta.appendChild(texto);
    tarjeta.appendChild(boton);

    columna.appendChild(tarjeta);

    lista.appendChild(columna);

    contador++;
    total.textContent = contador;

    formulario.reset();
});