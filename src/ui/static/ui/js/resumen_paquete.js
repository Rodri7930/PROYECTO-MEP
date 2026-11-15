
document.addEventListener("DOMContentLoaded", () => {
    const CLAVE = "mep_paquetes_demo";
    const parametros = new URLSearchParams(window.location.search);
    const idPaquete = parametros.get("id");

    let paquetes = [];

    try {
        paquetes = JSON.parse(sessionStorage.getItem(CLAVE) || "[]");
    } catch {
        paquetes = [];
    }

    const paquete = paquetes.find(
        (item) => item.id === idPaquete
    );

    if (!paquete) {
        document.querySelector(".resumen-datos").hidden = true;
        document.querySelector(".resumen-proveedores").hidden = true;
        document.getElementById("error-resumen").hidden = false;
        return;
    }

    function mostrar(id, valor) {
        document.getElementById(id).textContent = valor;
    }

    mostrar("resumen-nombre", paquete.nombre);
    mostrar("resumen-tipo", paquete.tipo);
    mostrar("resumen-destino", paquete.destino);
    mostrar("resumen-duracion", `${paquete.duracion} días`);
    mostrar("resumen-pasajeros", paquete.pasajeros);

    const costo = paquete.costo_objetivo;

    mostrar(
        "resumen-costo",
        costo === null || costo === undefined
            ? "No especificado"
            : `USD ${Number(costo).toFixed(2)}`
    );

    const proveedores = paquete.proveedores || [];
    const lista = document.getElementById("lista-proveedores");

    if (proveedores.length > 0) {
        document.getElementById("mensaje-proveedores").hidden = true;

        proveedores.forEach((proveedor) => {
            const elemento = document.createElement("p");
            elemento.textContent = proveedor.nombre;
            lista.appendChild(elemento);
        });
    }
});
