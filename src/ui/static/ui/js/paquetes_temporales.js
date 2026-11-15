
document.addEventListener("DOMContentLoaded", () => {
    const CLAVE = "mep_paquetes_demo";

    function obtenerPaquetes() {
        try {
            return JSON.parse(sessionStorage.getItem(CLAVE) || "[]");
        } catch {
            return [];
        }
    }

    function guardarPaquetes(paquetes) {
        sessionStorage.setItem(CLAVE, JSON.stringify(paquetes));
    }


    // MODO EDICIÓN: IDENTIFICAR EL PAQUETE

    const parametrosEdicion = new URLSearchParams(window.location.search);
    const idEdicion = parametrosEdicion.get("editar");

    const paqueteEdicion = idEdicion
        ? obtenerPaquetes().find((paquete) => paquete.id === idEdicion)
        : null;

    function cargarDatosEdicion(formulario, paquete) {
        if (!formulario || !paquete) {
            return;
        }

        const campos = {
            destino: paquete.destino,
            duracion: paquete.duracion,
            pasajeros: paquete.pasajeros,
            costo_objetivo: paquete.costo_objetivo,
            cliente_referencia: paquete.cliente_referencia,
            cambio_solicitado: paquete.cambio_solicitado
        };

        Object.entries(campos).forEach(([nombre, valor]) => {
            const campo = formulario.elements.namedItem(nombre);

            if (campo && valor !== undefined && valor !== null) {
                campo.value = valor;
            }
        });

        // Nombre del paquete
        const campoNombre = formulario.elements.namedItem("nombre");

        if (campoNombre) {
            if (campoNombre.tagName === "SELECT") {
                campoNombre.value =
                    paquete.paquete_original_id || paquete.id;
            } else {
                campoNombre.value = paquete.nombre;
            }
        }

        const botonRegistrar = formulario.querySelector(
            'button[type="submit"]'
        );

        if (botonRegistrar) {
            botonRegistrar.textContent = "Guardar cambios";
        }
    }

    // CARGAR PAQUETES EN PERSONALIZAR

    const formularioPersonalizar = document.getElementById(
        "form-personalizar-paquete"
    );


if (formularioPersonalizar) {
    const selector = formularioPersonalizar.querySelector('[name="nombre"]');

    const campoCliente = formularioPersonalizar.querySelector(
        '[name="cliente_referencia"]'
    );
    const campoCambio = formularioPersonalizar.querySelector(
        '[name="cambio_solicitado"]'
    );
    const campoDestino = formularioPersonalizar.querySelector(
        '[name="destino"]'
    );
    const campoDuracion = formularioPersonalizar.querySelector(
        '[name="duracion"]'
    );
    const campoPasajeros = formularioPersonalizar.querySelector(
        '[name="pasajeros"]'
    );
    const campoCosto = formularioPersonalizar.querySelector(
        '[name="costo_objetivo"]'
    );

    const paquetes = obtenerPaquetes();

    // Mostrar únicamente paquetes originales como punto de partida.
    if (selector) {
        selector.replaceChildren();

        const opcionInicial = document.createElement("option");
        opcionInicial.value = "";
        opcionInicial.textContent = "Selecciona un paquete guardado";
        selector.appendChild(opcionInicial);

        paquetes
            .filter((paquete) => paquete.tipo !== "Personalizado")
            .forEach((paquete) => {
                const opcion = document.createElement("option");
                opcion.value = paquete.id;
                opcion.textContent = paquete.nombre;
                selector.appendChild(opcion);
            });

        // Autocompletar los datos al seleccionar un paquete.
        selector.addEventListener("change", () => {
            const paqueteSeleccionado = paquetes.find(
                (paquete) => paquete.id === selector.value
            );

            if (!paqueteSeleccionado) {
                return;
            }

            campoDestino.value = paqueteSeleccionado.destino || "";
            campoDuracion.value = paqueteSeleccionado.duracion || 1;
            campoPasajeros.value = paqueteSeleccionado.pasajeros || 1;
            campoCosto.value = paqueteSeleccionado.costo_objetivo ?? "";
        });

        // Cargar datos cuando editamos un paquete personalizado.
        if (paqueteEdicion && paqueteEdicion.tipo === "Personalizado") {
            cargarDatosEdicion(formularioPersonalizar, paqueteEdicion);
        }
    }

    // Guardar la versión personalizada.
    formularioPersonalizar.addEventListener("submit", (evento) => {
        evento.preventDefault();

        if (!formularioPersonalizar.reportValidity()) {
            return;
        }

        const paqueteOriginal = paquetes.find(
            (paquete) => paquete.id === selector.value
        );

        if (!paqueteOriginal) {
            alert("Debes seleccionar un paquete registrado.");
            return;
        }

        const cliente = campoCliente.value.trim();
        const cambio = campoCambio.value.trim();

        if (!cliente || !cambio) {
            alert("Completa el cliente y el cambio solicitado.");
            return;
        }

        // Validar duración, pasajeros y costo objetivo.

        const duracion = Number(campoDuracion.value);
        const pasajeros = Number(campoPasajeros.value);

        const costoTexto = campoCosto.value.trim();
        const costo = costoTexto === "" ? null : Number(costoTexto);

        if (!Number.isInteger(duracion) || duracion < 1) {
            alert("La duración debe ser de al menos 1 día.");
            campoDuracion.focus();
            return;
        }

        if (!Number.isInteger(pasajeros) || pasajeros < 1) {
            alert("Debe registrarse al menos 1 pasajero.");
            campoPasajeros.focus();
            return;
        }

        if (
            costo !== null &&
            (!Number.isFinite(costo) || costo < 0)
        ) {
            alert("El costo objetivo no puede ser negativo.");
            campoCosto.focus();
            return;
        }

        const paquetesActualizados = obtenerPaquetes();

        if (idEdicion) {
            // EDITAR PAQUETE PERSONALIZADO
            const indice = paquetesActualizados.findIndex(
                (item) => item.id === idEdicion && item.tipo === "Personalizado"
            );

            if (indice === -1) {
                alert("No se encontró el paquete personalizado.");
                return;
            }

            paquetesActualizados[indice] = {
                ...paquetesActualizados[indice],
                nombre: `${paqueteOriginal.nombre} - Personalizado`,
                destino: campoDestino.value,
                duracion,
                pasajeros,
                costo_objetivo: costo,
                cliente_referencia: cliente,
                cambio_solicitado: cambio,
                paquete_original_id: paqueteOriginal.id
            };

            try {
                guardarPaquetes(paquetesActualizados);
            } catch {
                alert("No se pudieron guardar los cambios.");
                return;
            }

            alert("Los cambios del paquete personalizado se guardaron correctamente.");

            window.location.href =
                `/reservas/resumen/?id=${encodeURIComponent(idEdicion)}`;
        } else {
            // REGISTRAR UN NUEVO PAQUETE PERSONALIZADO
            const nuevoPaquete = {
                id: `demo-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
                nombre: `${paqueteOriginal.nombre} - Personalizado`,
                destino: campoDestino.value,
                duracion,
                pasajeros,
                costo_objetivo: costo,
                cliente_referencia: cliente,
                cambio_solicitado: cambio,
                paquete_original_id: paqueteOriginal.id,
                tipo: "Personalizado",
                estado: "En revisión",
                proveedores: []
            };

            paquetesActualizados.push(nuevoPaquete);

            try {
                guardarPaquetes(paquetesActualizados);
            } catch {
                alert("No se pudo guardar el paquete personalizado.");
                return;
            }

            alert(
                `El paquete "${nuevoPaquete.nombre}" se registró correctamente.`
            );

            window.location.href = "/reservas/";
        }

    });
}

    // REGISTRAR PAQUETE DEMOSTRATIVO

    const formulario = document.getElementById("form-nuevo-paquete");

    if (formulario) {

        if (paqueteEdicion && paqueteEdicion.tipo !== "Personalizado") {
            cargarDatosEdicion(formulario, paqueteEdicion);
        }

        formulario.addEventListener("submit", (evento) => {
            evento.preventDefault();

            if (!formulario.reportValidity()) {
                return;
            }

            const datos = new FormData(formulario);

            const nombre = String(datos.get("nombre") || "").trim();
            const destino = String(datos.get("destino") || "").trim();
            const duracion = Number(datos.get("duracion"));
            const pasajeros = Number(datos.get("pasajeros"));
            const costoTexto = String(
                datos.get("costo_objetivo") || ""
            ).trim();

            const costo = costoTexto === "" ? null : Number(costoTexto);

            if (
                !nombre ||
                !destino ||
                !Number.isInteger(duracion) ||
                duracion < 1 ||
                !Number.isInteger(pasajeros) ||
                pasajeros < 1 ||
                (costo !== null && (!Number.isFinite(costo) || costo < 0))
            ) {
                alert("Revisa los datos ingresados.");
                return;
            }

            const paquetes = obtenerPaquetes();

            if (idEdicion) {
                // EDITAR: actualizar el registro existente.
                const indice = paquetes.findIndex(
                    (item) => item.id === idEdicion && item.tipo !== "Personalizado"
                );

                if (indice === -1) {
                    alert("No se encontró el paquete que deseas editar.");
                    return;
                }

                paquetes[indice] = {
                    ...paquetes[indice],
                    nombre,
                    destino,
                    duracion,
                    pasajeros,
                    costo_objetivo: costo
                };

                try {
                    guardarPaquetes(paquetes);
                } catch {
                    alert("No se pudieron guardar los cambios.");
                    return;
                }

                alert("Los cambios del paquete se guardaron correctamente.");

                window.location.href =
                    `/reservas/resumen/?id=${encodeURIComponent(idEdicion)}`;
            } else {
                // REGISTRAR: crear un paquete nuevo.
                const paquete = {
                    id: `demo-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
                    nombre,
                    destino,
                    duracion,
                    pasajeros,
                    costo_objetivo: costo,
                    tipo: "Nuevo",
                    estado: "En preparación"
                };

                paquetes.push(paquete);

                try {
                    guardarPaquetes(paquetes);
                } catch {
                    alert("No se pudo guardar el paquete temporalmente.");
                    return;
                }

                alert(
                    `El paquete "${paquete.nombre}" se registró correctamente.`
                );

                window.location.href = "/reservas/";
            }

        });
    }

    // MOSTRAR PAQUETES EN RESERVAS

    const tabla = document.getElementById("tabla-paquetes");

    if (tabla) {
        const cuerpo = tabla.querySelector("tbody");
        const paquetes = obtenerPaquetes();

        if (!cuerpo || paquetes.length === 0) {
            return;
        }

        cuerpo.replaceChildren();

        paquetes.forEach((paquete) => {
            const fila = document.createElement("tr");

            const nombre = document.createElement("td");
            nombre.textContent = paquete.nombre;

            const tipo = document.createElement("td");
            tipo.textContent = paquete.tipo;

            const estado = document.createElement("td");
            estado.textContent = paquete.estado;

            const acciones = document.createElement("td");

            const resumen = document.createElement("a");
            resumen.href = `/reservas/resumen/?id=${encodeURIComponent(paquete.id)}`;
            resumen.textContent = "Ver resumen";
            resumen.className = "boton-secundario boton-tabla";

            const comparar = document.createElement("a");

            comparar.href =
                `/reservas/comparar/?id=${encodeURIComponent(paquete.id)}`;

            comparar.textContent = "Comparar";
            comparar.className = "boton-principal boton-tabla";

            acciones.append(resumen, " ", comparar);

            fila.append(nombre, tipo, estado, acciones);
            cuerpo.appendChild(fila);
        });
    }
});
