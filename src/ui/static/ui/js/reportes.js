
document.addEventListener("DOMContentLoaded", () => {
    const CLAVE = "mep_paquetes_demo";

    const filtroEstado = document.getElementById("filtro-estado");
    const filtroTipo = document.getElementById("filtro-tipo");
    const listado = document.getElementById("listado-reportes");
    const contador = document.getElementById("contador-reportes");
    const botonCSV = document.getElementById("exportar-csv");
    const botonPDF = document.getElementById("exportar-pdf");

    if (
        !filtroEstado || !filtroTipo || !listado ||
        !contador || !botonCSV || !botonPDF
    ) {
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

    function obtenerFiltrados() {
        return paquetes.filter((paquete) => {
            const cumpleEstado =
                !filtroEstado.value ||
                paquete.estado === filtroEstado.value;

            const cumpleTipo =
                !filtroTipo.value ||
                paquete.tipo === filtroTipo.value;

            return cumpleEstado && cumpleTipo;
        });
    }

    function agregarDato(contenedor, etiqueta, valor) {
        const parrafo = document.createElement("p");

        const titulo = document.createElement("strong");
        titulo.textContent = `${etiqueta}: `;

        const contenido = document.createTextNode(
            String(valor ?? "No especificado")
        );

        parrafo.append(titulo, contenido);
        contenedor.appendChild(parrafo);
    }

    function mostrarReportes() {
        const filtrados = obtenerFiltrados();

        listado.replaceChildren();

        contador.textContent =
            `${filtrados.length} paquete(s) encontrado(s)`;

        if (filtrados.length === 0) {
            const mensaje = document.createElement("p");
            mensaje.textContent =
                "No se encontraron paquetes con los filtros seleccionados.";

            listado.appendChild(mensaje);
            return;
        }

        filtrados.forEach((paquete) => {
            const desplegable = document.createElement("details");
            desplegable.className = "reporte-paquete";

            const encabezado = document.createElement("summary");

            const nombre = document.createElement("strong");
            nombre.textContent = paquete.nombre;

            const estado = document.createElement("span");
            estado.textContent = paquete.estado || "Sin estado";
            estado.className = "estado-reporte";

            encabezado.append(nombre, estado);

            const detalle = document.createElement("div");
            detalle.className = "detalle-reporte";

            agregarDato(detalle, "Tipo", paquete.tipo);
            agregarDato(detalle, "Destino", paquete.destino);
            agregarDato(detalle, "Duración", `${paquete.duracion} días`);
            agregarDato(detalle, "Pasajeros", paquete.pasajeros);

            const costo = paquete.costo_objetivo;
            agregarDato(
                detalle,
                "Costo objetivo",
                costo === null || costo === undefined || costo === ""
                    ? "No especificado"
                    : `USD ${Number(costo).toFixed(2)}`
            );

            if (paquete.tipo === "Personalizado") {
                agregarDato(
                    detalle,
                    "Cliente",
                    paquete.cliente_referencia
                );

                agregarDato(
                    detalle,
                    "WhatsApp",
                    paquete.contacto_cliente || "Sin contacto"
                );

                agregarDato(
                    detalle,
                    "Cambio solicitado",
                    paquete.cambio_solicitado
                );
            }

            const proveedores = Array.isArray(paquete.proveedores)
                ? paquete.proveedores
                : [];

            const subtitulo = document.createElement("h3");
            subtitulo.textContent =
                `Proveedores seleccionados (${proveedores.length})`;

            detalle.appendChild(subtitulo);

            if (proveedores.length === 0) {
                const mensaje = document.createElement("p");
                mensaje.textContent =
                    "Todavía no tiene proveedores seleccionados.";

                detalle.appendChild(mensaje);
            } else {
                const lista = document.createElement("ul");

                proveedores.forEach((proveedor) => {
                    const elemento = document.createElement("li");

                    elemento.textContent =
                        `${proveedor.nombre} — ${proveedor.servicio} — ` +
                        `USD ${Number(proveedor.tarifa).toFixed(2)}`;

                    lista.appendChild(elemento);
                });

                detalle.appendChild(lista);
            }

            const enlace = document.createElement("a");

            enlace.href =
                `/reservas/resumen/?id=${encodeURIComponent(paquete.id)}`;

            enlace.textContent = "Ver resumen del paquete";
            enlace.className = "enlace-reporte";

            detalle.appendChild(enlace);

            desplegable.append(encabezado, detalle);
            listado.appendChild(desplegable);
        });
    }

    // EXPORTAR CSV

    function escaparCSV(valor) {
        let texto = String(valor ?? "");

        // Evitar que hojas de cálculo interpreten texto como fórmula.
        if (/^[\s]*[=+\-@\t\r]/.test(texto)) {
            texto = `'${texto}`;
        }

        return `"${texto.replace(/"/g, '""')}"`;
    }

    botonCSV.addEventListener("click", () => {
        const filtrados = obtenerFiltrados();

        if (filtrados.length === 0) {
            alert("No hay paquetes para exportar.");
            return;
        }

        const filas = [
            [
                "Paquete",
                "Tipo",
                "Estado",
                "Destino",
                "Duracion",
                "Pasajeros",
                "Costo objetivo USD",
                "Cliente",
                "WhatsApp",
                "Proveedores seleccionados"
            ]
        ];

        filtrados.forEach((paquete) => {
            const proveedores = Array.isArray(paquete.proveedores)
                ? paquete.proveedores
                : [];

            filas.push([
                paquete.nombre,
                paquete.tipo,
                paquete.estado,
                paquete.destino,
                paquete.duracion,
                paquete.pasajeros,
                paquete.costo_objetivo ?? "",
                paquete.cliente_referencia ?? "",
                paquete.contacto_cliente ?? "",
                proveedores.map((p) => p.nombre).join("; ")
            ]);
        });

        const contenido = filas
            .map((fila) => fila.map(escaparCSV).join(","))
            .join("\r\n");

        const archivo = new Blob(
            ["\uFEFF", contenido],
            { type: "text/csv;charset=utf-8;" }
        );

        const url = URL.createObjectURL(archivo);
        const enlace = document.createElement("a");

        enlace.href = url;
        enlace.download = "reporte_paquetes_mep.csv";

        document.body.appendChild(enlace);
        enlace.click();
        enlace.remove();

        setTimeout(() => URL.revokeObjectURL(url), 1000);
    });

    // EXPORTAR PDF MEDIANTE IMPRESIÓN DEL NAVEGADOR

    botonPDF.addEventListener("click", () => {
        if (obtenerFiltrados().length === 0) {
            alert("No hay paquetes para exportar.");
            return;
        }

        const desplegables = Array.from(
            listado.querySelectorAll("details")
        );

        const abiertosOriginalmente = desplegables.map(
            (elemento) => elemento.open
        );

        desplegables.forEach((elemento) => {
            elemento.open = true;
        });

        const restaurar = () => {
            desplegables.forEach((elemento, indice) => {
                elemento.open = abiertosOriginalmente[indice];
            });

            window.removeEventListener("afterprint", restaurar);
        };

        window.addEventListener("afterprint", restaurar);
        window.print();
    });

    filtroEstado.addEventListener("change", mostrarReportes);
    filtroTipo.addEventListener("change", mostrarReportes);

    mostrarReportes();
});
