
document.addEventListener("DOMContentLoaded", () => {
    const CLAVE = "mep_paquetes_demo";

    const buscador = document.getElementById("buscar-cliente");
    const contador = document.getElementById("contador-clientes");
    const tabla = document.getElementById("tabla-clientes");

    if (!buscador || !contador || !tabla) {
        return;
    }

    const cuerpo = tabla.querySelector("tbody");

    if (!cuerpo) {
        return;
    }

    let paquetes = [];

    try {
        const datos = JSON.parse(
            sessionStorage.getItem(CLAVE) || "[]"
        );

        paquetes = Array.isArray(datos) ? datos : [];
    } catch {
        paquetes = [];
    }

    // Obtener clientes de los paquetes personalizados.
    const idsRegistrados = new Set();

    const clientes = paquetes
        .filter((paquete) => {
            if (
                paquete.tipo !== "Personalizado" ||
                !paquete.cliente_referencia ||
                !paquete.id ||
                idsRegistrados.has(paquete.id)
            ) {
                return false;
            }

            idsRegistrados.add(paquete.id);
            return true;
        })
        .map((paquete) => ({
            nombre: paquete.cliente_referencia,
            contacto: paquete.contacto_cliente || "Sin contacto",
            paquete: paquete.nombre,
            idPaquete: paquete.id
        }));

    function mostrarClientes(textoBusqueda = "") {
        const busqueda = textoBusqueda.trim().toLowerCase();

        const filtrados = clientes.filter((cliente) => {
            const contenido =
                `${cliente.nombre} ${cliente.contacto} ${cliente.paquete}`
                    .toLowerCase();

            return contenido.includes(busqueda);
        });

        cuerpo.replaceChildren();

        contador.textContent = `${filtrados.length} cliente(s)`;

        if (filtrados.length === 0) {
            const fila = document.createElement("tr");
            const celda = document.createElement("td");

            celda.colSpan = 3;
            celda.textContent = busqueda
                ? "No se encontraron clientes con esa búsqueda."
                : "Todavía no hay clientes registrados.";

            fila.appendChild(celda);
            cuerpo.appendChild(fila);
            return;
        }

        filtrados.forEach((cliente) => {
            const fila = document.createElement("tr");

            const celdaNombre = document.createElement("td");
            celdaNombre.textContent = cliente.nombre;

            const celdaContacto = document.createElement("td");
            celdaContacto.textContent = cliente.contacto;

            const celdaPaquete = document.createElement("td");
            const enlace = document.createElement("a");

            enlace.href =
                `/reservas/resumen/?id=${encodeURIComponent(cliente.idPaquete)}`;

            enlace.textContent = cliente.paquete;

            celdaPaquete.appendChild(enlace);
            fila.append(celdaNombre, celdaContacto, celdaPaquete);
            cuerpo.appendChild(fila);
        });
    }

    buscador.addEventListener("input", () => {
        mostrarClientes(buscador.value);
    });

    mostrarClientes();
});
