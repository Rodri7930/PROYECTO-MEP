
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
        informacion.textContent = "No se encontró el paquete seleccionado.";
        formulario.hidden = true;
        return;
    }

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
        verResumen.textContent =
            `Ver resumen del paquete (${paquete.proveedores.length} elegidos)`;
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

    function crearBoton(texto, accion) {
        const boton = document.createElement("button");
        boton.type = "button";
        boton.textContent = texto;
        boton.className = "boton-secundario";
        boton.addEventListener("click", accion);
        return boton;
    }

    function mostrarProveedores(proveedores, limite) {
        tabla.replaceChildren();

        if (proveedores.length === 0) {
            const fila = document.createElement("tr");
            const celda = document.createElement("td");

            celda.colSpan = 5;
            celda.className = "tabla-vacia";
            celda.textContent =
                "No se encontraron tarifas registradas para estos filtros.";

            fila.appendChild(celda);
            tabla.appendChild(fila);
            return;
        }

        proveedores.forEach((proveedor, indice) => {
            const seleccionado = paquete.proveedores.some(
                (item) => Number(item.id) === Number(proveedor.id)
            );

            const fila = document.createElement("tr");

            const valores = [
                indice + 1,
                proveedor.nombre,
                proveedor.detalle,
                `${proveedor.moneda} ${proveedor.tarifa.toFixed(2)}`
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
                        (item) => Number(item.id) === Number(proveedor.id)
                    );

                    if (yaSeleccionado) {
                        return;
                    }

                    const cantidadServicio = paquete.proveedores.filter(
                        (item) => item.servicio === proveedor.servicio
                    ).length;

                    if (cantidadServicio >= limite) {
                        alert(
                            `Puedes seleccionar hasta ${limite} proveedores de este servicio.`
                        );
                        return;
                    }

                    paquete.proveedores.push({ ...proveedor });
                    guardarSeleccion();
                    mostrarProveedores(proveedores, limite);
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
                    `${proveedor.nombre} · ${proveedor.servicio}`;

                const informacionDetalle = document.createElement("p");
                informacionDetalle.textContent =
                    `Tarifa referencial: ${proveedor.moneda} ` +
                    `${proveedor.tarifa.toFixed(2)}`;

                const quitar = crearBoton("Quitar", () => {
                    paquete.proveedores = paquete.proveedores.filter(
                        (item) => Number(item.id) !== Number(proveedor.id)
                    );

                    guardarSeleccion();
                    mostrarProveedores(proveedores, limite);
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

    formulario.addEventListener("submit", async (evento) => {
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

        const parametros = new URLSearchParams({
            servicio,
            temporada,
            pasajeros: String(paquete.pasajeros),
            cantidad: String(cantidad),
            fecha: new Date().toISOString().slice(0, 10)
        });

        if (tarifaMaxima !== null) {
            parametros.set("tarifa_maxima", String(tarifaMaxima));
        }

        const botonConsultar = formulario.querySelector(
            'button[type="submit"]'
        );

        botonConsultar.disabled = true;
        botonConsultar.textContent = "Consultando...";
        resultados.hidden = false;
        mensaje.textContent = "Consultando tarifas registradas...";

        try {
            const respuesta = await fetch(
                `/api/comparar-tarifas/?${parametros.toString()}`
            );

            const datos = await respuesta.json();

            if (!respuesta.ok) {
                throw new Error(datos.error || "No se pudo consultar.");
            }

            const proveedores = datos.resultados.map((item) => ({
                ...item,
                tarifa: Number(item.tarifa)
            }));

            mostrarProveedores(proveedores, cantidad);

            mensaje.textContent = proveedores.length
                ? `Se encontraron ${proveedores.length} tarifas reales para ${servicio}, temporada ${temporada}.`
                : `No existen tarifas registradas para ${servicio}, temporada ${temporada}, con estos filtros.`;

        } catch (error) {
            tabla.replaceChildren();
            mensaje.textContent = error.message;
        } finally {
            botonConsultar.disabled = false;
            botonConsultar.textContent = "Consultar tarifas";
        }
    });
});
