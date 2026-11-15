document.addEventListener("DOMContentLoaded", () => {
    const botonSalir = document.getElementById("boton-salir");

    if (!botonSalir) {
        return;
    }

    botonSalir.addEventListener("click", (evento) => {
        evento.preventDefault();

        // Eliminar únicamente la sesión demostrativa.
        sessionStorage.removeItem("mep_sesion_demo");

        // Volver al inicio de sesión.
        window.location.replace("/login/");
    });
});