
document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("form-login");
    const usuario = document.getElementById("usuario-login");
    const contrasena = document.getElementById("contrasena-login");
    const mensaje = document.getElementById("mensaje-login");

    // Si ya existe una sesión demostrativa, regresar a Inicio.
    if (sessionStorage.getItem("mep_sesion_demo")) {
        window.location.replace("/inicio/");
        return;
    }

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();

        const correo = usuario.value.trim();
        const clave = contrasena.value;

        mensaje.hidden = true;

        // Correo válido: incluye @ y un dominio.
        const correoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);

        if (!correoValido) {
            mensaje.textContent = "Ingresa un correo electrónico válido.";
            mensaje.hidden = false;
            usuario.focus();
            return;
        }

        if (clave.trim() === "") {
            mensaje.textContent = "Ingresa una contraseña.";
            mensaje.hidden = false;
            contrasena.focus();
            return;
        }

        // Sesión demostrativa, sin guardar contraseñas.
        sessionStorage.setItem("mep_sesion_demo", correo);

        window.location.replace("/inicio/");
    });
});
