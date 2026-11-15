
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

    // REGISTRAR PAQUETE DEMOSTRATIVO

    const formulario = document.getElementById("form-nuevo-paquete");

    if (formulario) {
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

            const paquete = {
                id: `demo-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
                nombre,
                destino,
                duracion,
                pasajeros,
                costo_objetivo: costo,
                tipo: "Nuevo",
                estado: "En preparación",
            };

            const paquetes = obtenerPaquetes();
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
