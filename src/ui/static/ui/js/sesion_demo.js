
document.addEventListener("DOMContentLoaded", () => {
    const botonSalir = document.getElementById("boton-salir");

    if (botonSalir) {
        botonSalir.addEventListener("click", () => {
            sessionStorage.removeItem("mep_sesion_demo");
        });
    }
});
