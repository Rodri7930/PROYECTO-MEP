
document.addEventListener("DOMContentLoaded", () => {
    const tabla = document.getElementById("tabla-trabajos-recientes");

    if (!tabla) {
        return;
    }

    const cuerpo = tabla.querySelector("tbody");

    if (!cuerpo) {
        return;
    }

    let paquetes = [];

    try {
        const datos = JSON.parse(
            sessionStorage.getItem("mep_paquetes_demo") || "[]"
        );

        paquetes = Array.isArray(datos) ? datos : [];
    } catch {
        paquetes = [];
    }

    cuerpo.replaceChildren();

    if (paquetes.length === 0) {
        const fila = document.createElement("tr");
        const celda = document.createElement("td");

        celda.colSpan = 3;
        celda.textContent = "Todavía no hay trabajos recientes.";

        fila.appendChild(celda);
        cuerpo.appendChild(fila);
        return;
    }

    // Mostrar los cinco registros más recientes.
    const recientes = paquetes.slice(-5).reverse();

    recientes.forEach((paquete) => {
        const fila = document.createElement("tr");

        const nombre = document.createElement("td");
        const enlace = document.createElement("a");

        enlace.href =
            `/reservas/resumen/?id=${encodeURIComponent(paquete.id)}`;
        enlace.textContent = paquete.nombre;

        nombre.appendChild(enlace);

        const proximaTarea = document.createElement("td");

        proximaTarea.textContent =
            paquete.tipo === "Personalizado"
                ? "Revisar personalización"
                : "Comparar proveedores";

        const estado = document.createElement("td");
        estado.textContent = paquete.estado || "En preparación";

        fila.append(nombre, proximaTarea, estado);
        cuerpo.appendChild(fila);
    });
});
