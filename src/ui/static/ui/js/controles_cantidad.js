
"use strict";

document.addEventListener("DOMContentLoaded", function () {
    const botones = document.querySelectorAll(".boton-cantidad");

    botones.forEach(function (boton) {
        boton.addEventListener("click", function () {
            const idCampo = boton.getAttribute("data-campo");
            const accion = boton.getAttribute("data-accion");
            const campo = document.getElementById(idCampo);

            if (!campo || campo.disabled || campo.readOnly) {
                return;
            }

            const minimo = Number(campo.min) || 1;
            const valorActual = Number(campo.value) || minimo;

            if (accion === "sumar") {
                campo.value = valorActual + 1;
            }

            if (accion === "restar") {
                campo.value = Math.max(minimo, valorActual - 1);
            }

            campo.dispatchEvent(
                new Event("change", { bubbles: true })
            );
        });
    });
});
