
document.addEventListener("DOMContentLoaded", () => {
    const CLAVE_PAQUETES = "mep_paquetes_demo";

    const parametros = new URLSearchParams(window.location.search);
    const idPaquete = parametros.get("id");

    const formulario = document.getElementById("form-comparacion");
    const informacion = document.getElementById("informacion-paquete");
    const resultados = document.getElementById("resultados-comparacion");
    const tabla = document.getElementById("tabla-resultados");
    const mensaje = document.getElementById("mensaje-comparacion");
    const volver = document.getElementById("volver-resumen");
    const verResumen = document.getElementById("ver-resumen-comparacion");

    let paquetes = [];

    try {
        paquetes = JSON.parse(
            sessionStorage.getItem(CLAVE_PAQUETES) || "[]"
        );
    } catch {
        paquetes = [];
    }

    const paquete = paquetes.find((item) => item.id === idPaquete);

    if (!paquete) {
        informacion.textContent =
            "No se encontró el paquete seleccionado.";
        formulario.hidden = true;
        return;
    }

    // Proveedores seleccionados para este paquete.
    if (!Array.isArray(paquete.proveedores)) {
        paquete.proveedores = [];
    }

    function guardarSeleccion() {
        sessionStorage.setItem(
            CLAVE_PAQUETES,
            JSON.stringify(paquetes)
        );
        actualizarContador();
    }

    function actualizarContador() {
        const cantidad = paquete.proveedores.length;

        verResumen.textContent =
            `Ver resumen del paquete (${cantidad} elegidos)`;
    }

    actualizarContador();


    const urlResumen =
        `/reservas/resumen/?id=${encodeURIComponent(paquete.id)}`;

    volver.href = urlResumen;
    verResumen.href = urlResumen;

    const costo = paquete.costo_objetivo;

    const textoCosto =
        costo === null || costo === undefined
            ? "Sin costo objetivo"
            : `USD ${Number(costo).toFixed(2)}`;

    informacion.textContent =
        `Paquete: ${paquete.nombre} · ` +
        `${paquete.pasajeros} pasajeros · ` +
        `${paquete.duracion} días · ` +
        `Costo objetivo ${textoCosto}`;

    // CATÁLOGO DEMOSTRATIVO

    const servicios = {
        "Hospedaje": {
            nombres: [
                "Hotel Inti",
                "Hotel Andino",
                "Hotel Imperial II",
                "Hotel Cusco",
                "Hotel Sol",
            ],
            detalle: "Habitación doble",
            base: 75,
            unidad: "habitación/noche",
        },
        "Alimentación": {
            nombres: [
                "Restaurante Inti",
                "Restaurante Andino",
                "Restaurante Imperial",
                "Restaurante Cusco",
                "Restaurante Sol",
            ],
            detalle: "Menú turístico",
            base: 18,
            unidad: "persona",
        },
        "Transporte": {
            nombres: [
                "Transportes Inti",
                "Transportes Andinos",
                "Transporte Imperial",
                "Transporte Cusco",
                "Transporte Sol",
            ],
            detalle: "Servicio de transporte turístico",
            base: 55,
            unidad: "servicio",
        },
        "Guiado": {
            nombres: [
                "Guías Inti",
                "Guías Andinos",
                "Guías Imperial",
                "Guías Cusco",
                "Guías Sol",
            ],
            detalle: "Servicio de guiado turístico",
            base: 40,
            unidad: "servicio",
        },
        "Tren y entradas": {
            nombres: [
                "Operador Inti",
                "Operador Andino",
                "Operador Imperial",
                "Operador Cusco",
                "Operador Sol",
            ],
            detalle: "Tren y entradas turísticas",
            base: 110,
            unidad: "persona",
        },
    };

    const factoresTemporada = {
        Alta: 1.25,
        Media: 1,
        Baja: 0.85,
    };

    function obtenerProveedores(servicio, temporada) {
        const configuracion = servicios[servicio];
        const factor = factoresTemporada[temporada];

        if (!configuracion || !factor) {
            return [];
        }

        return Array.from({ length: 20 }, (_, indice) => {
            const numero = indice + 1;

            const nombreBase =
                configuracion.nombres[indice % 5];

            const nombre =
                indice < 5
                    ? nombreBase
                    : `${nombreBase} ${Math.floor(indice / 5) + 1}`;

            const tarifaBase =
                configuracion.base + indice * 3.5;

            const tarifa = Number(
                (tarifaBase * factor).toFixed(2)
            );

            return {
                id: `${servicio}-${numero}`,
                nombre,
                servicio,
                detalle: configuracion.detalle,
                tarifa,
                unidad: configuracion.unidad,
            };
        });
    }



    function crearBoton(texto, accion) {
        const boton = document.createElement("button");
        boton.type = "button";
        boton.textContent = texto;
        boton.className = "boton-secundario";
        boton.addEventListener("click", accion);
        return boton;
    }

    function mostrarProveedores(proveedores, catalogo, limite) {
        tabla.replaceChildren();

        if (proveedores.length === 0) {
            const fila = document.createElement("tr");
            const celda = document.createElement("td");

            celda.colSpan = 5;
            celda.className = "tabla-vacia";
            celda.textContent =
                "No se encontraron proveedores para estos filtros.";

            fila.appendChild(celda);
            tabla.appendChild(fila);
            return;
        }

        const promedio = catalogo.reduce(
            (total, item) => total + item.tarifa,
            0
        ) / catalogo.length;

        proveedores.forEach((proveedor, indice) => {
            const seleccionado = paquete.proveedores.some(
                (item) => item.id === proveedor.id
            );

            const fila = document.createElement("tr");

            const valores = [
                indice + 1,
                proveedor.nombre,
                proveedor.detalle,
                `USD ${proveedor.tarifa.toFixed(2)} · ${proveedor.unidad}`
            ];

            valores.forEach((valor) => {
                const celda = document.createElement("td");
                celda.textContent = valor;
                fila.appendChild(celda);
            });

            const accion = document.createElement("td");

            const boton = crearBoton(
                seleccionado ? "Seleccionado ✓" : "Seleccionar",
                () => {
                    const yaSeleccionado = paquete.proveedores.some(
                        (item) => item.id === proveedor.id
                    );

                    if (!yaSeleccionado) {
                        const cantidadServicio =
                            paquete.proveedores.filter(
                                (item) => item.servicio === proveedor.servicio
                            ).length;

                        if (cantidadServicio >= limite) {
                            alert(
                                `Puedes seleccionar hasta ${limite} proveedores de este servicio.`
                            );
                            return;
                        }

                        paquete.proveedores.push({
                            ...proveedor
                        });
                        guardarSeleccion();
                        mostrarProveedores(proveedores, catalogo, limite);
                    }
                }
            );

            boton.disabled = seleccionado;
            accion.appendChild(boton);
            fila.appendChild(accion);
            tabla.appendChild(fila);

            if (seleccionado) {
                const detalleFila = document.createElement("tr");
                detalleFila.className = "fila-detalle-proveedor";

                const detalleCelda = document.createElement("td");
                detalleCelda.colSpan = 5;

                const titulo = document.createElement("strong");
                titulo.textContent =
                    `${proveedor.nombre} · ${proveedor.servicio} · ${proveedor.detalle}`;

                const informacionDetalle = document.createElement("p");
                const ahorro = Math.max(
                    0,
                    promedio - proveedor.tarifa
                );

                informacionDetalle.textContent =
                    `Tarifa: USD ${proveedor.tarifa.toFixed(2)} ` +
                    `${proveedor.unidad} · ` +
                    `Ahorro estimado frente al promedio: USD ${ahorro.toFixed(2)}`;

                const quitar = crearBoton("Quitar", () => {
                    paquete.proveedores = paquete.proveedores.filter(
                        (item) => item.id !== proveedor.id
                    );

                    guardarSeleccion();
                    mostrarProveedores(proveedores, catalogo, limite);
                });

                detalleCelda.append(
                    titulo,
                    informacionDetalle,
                    quitar
                );

                detalleFila.appendChild(detalleCelda);
                tabla.appendChild(detalleFila);
            }
        });
    }

    // CONSULTAR TARIFAS

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();

        if (!formulario.reportValidity()) {
            return;
        }

        const servicio = document.getElementById("servicio").value;
        const temporada = document.getElementById("temporada").value;

        const tarifaTexto = document.getElementById(
            "tarifa-maxima"
        ).value.trim();

        const cantidad = Number(
            document.getElementById("cantidad-proveedores").value
        );

        const tarifaMaxima =
            tarifaTexto === "" ? null : Number(tarifaTexto);

        if (
            ![3, 5].includes(cantidad) ||
            (tarifaMaxima !== null &&
                (!Number.isFinite(tarifaMaxima) || tarifaMaxima < 0))
        ) {
            return;
        }

        const todos = obtenerProveedores(servicio, temporada);

        const elegibles = todos
            .filter((proveedor) =>
                tarifaMaxima === null ||
                proveedor.tarifa <= tarifaMaxima
            )
            .sort((a, b) => a.tarifa - b.tarifa);

        const recomendados = elegibles.slice(0, cantidad);

        mostrarProveedores(recomendados, elegibles, cantidad);

        const temporadaTexto = temporada.toLowerCase();

        mensaje.textContent =
            `Se compararon ${todos.length} proveedores de ` +
            `${servicio} (temporada ${temporadaTexto}); ` +
            `${elegibles.length} cumplen el rango. ` +
            `Se muestran los ${recomendados.length} más económicos.`;

        if (recomendados.length === 0) {
            const fila = document.createElement("tr");
            const celda = document.createElement("td");

            celda.colSpan = 5;
            celda.className = "tabla-vacia";
            celda.textContent =
                "No se encontraron proveedores para estos filtros.";

            fila.appendChild(celda);
            tabla.appendChild(fila);
        }

        resultados.hidden = false;
    });
});
