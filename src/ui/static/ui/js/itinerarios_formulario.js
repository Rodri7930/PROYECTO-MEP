
document.addEventListener("DOMContentLoaded", () => {
    const paquete = document.getElementById("paquete");
    const destino = document.getElementById("destino");
    const duracion = document.getElementById("duracion");
    const contenedor = document.getElementById("actividades-itinerario");
    const guardar = document.getElementById("guardar-itinerario");
    const mensaje = document.getElementById("mensaje-itinerario");

    function validarActividades() {
        const campos = contenedor.querySelectorAll("textarea");

        const formularioValido =
            paquete.value !== "" &&
            campos.length === Number(duracion.value) &&
            campos.length > 0 &&
            Array.from(campos).every((campo) => {
                const descripcion = campo.value.trim();

                return /[a-záéíóúüñ]/i.test(descripcion);
            });

        guardar.disabled = !formularioValido;

        return formularioValido;
    }

contenedor.addEventListener("input", () => {
    mensaje.hidden = true;
    validarActividades();
});

guardar.addEventListener("click", () => {
    if (!validarActividades()) {
        return;
    }

    mensaje.textContent =
        "Formulario validado correctamente. El guardado estará disponible cuando se integre la base de datos.";

    mensaje.hidden = false;
});


    if (!paquete || !destino || !duracion || !contenedor) {
        return;
    }

    paquete.addEventListener("change", () => {
        guardar.disabled = true;
        mensaje.hidden = true;
        const opcion = paquete.options[paquete.selectedIndex];

        destino.value = opcion.dataset.destino || "";
        duracion.value = opcion.dataset.duracion || "";

        contenedor.replaceChildren();

        const dias = Number(opcion.dataset.duracion || 0);

        if (!dias) {
            const mensaje = document.createElement("p");
            mensaje.textContent =
                "Selecciona un paquete turístico para visualizar los días correspondientes.";
            contenedor.appendChild(mensaje);
            return;
        }

        for (let dia = 1; dia <= dias; dia++) {
            const grupo = document.createElement("div");
            grupo.className = "grupo-campo";

            const etiqueta = document.createElement("label");
            etiqueta.htmlFor = `actividad-dia-${dia}`;
            etiqueta.textContent = `Día ${dia} *`;

            const campo = document.createElement("textarea");
            campo.id = `actividad-dia-${dia}`;
            campo.name = `actividad_dia_${dia}`;
            campo.className = "campo-formulario";
            campo.rows = 3;
            campo.required = true;
            campo.placeholder =
                `Describe las actividades del día ${dia}...`;

            grupo.append(etiqueta, campo);
            contenedor.appendChild(grupo);
        }
    });
});
