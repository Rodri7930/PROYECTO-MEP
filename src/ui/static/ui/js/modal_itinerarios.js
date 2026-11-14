
document.addEventListener("DOMContentLoaded", () => {
    const botonesAbrir = document.querySelectorAll(
        "[data-abrir-itinerario]"
    );

    botonesAbrir.forEach((boton) => {
        boton.addEventListener("click", () => {
            const idModal = boton.dataset.abrirItinerario;
            const modal = document.getElementById(idModal);

            if (modal) {
                modal.showModal();
            }
        });
    });

    const botonesCerrar = document.querySelectorAll(
        "[data-cerrar-itinerario]"
    );

    botonesCerrar.forEach((boton) => {
        boton.addEventListener("click", () => {
            const modal = boton.closest("dialog");

            if (modal) {
                modal.close();
            }
        });
    });
});
