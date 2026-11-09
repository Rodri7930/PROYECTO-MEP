"""Punto de entrada principal del Sistema Magic Experiences Perú (MEP).

Inicializa el entorno y ejecuta la verificación demostrativa de servicios.
"""

from demo_backend import main as ejecutar_demo


def main() -> None:
    print("==================================================================")
    print("  MAGIC EXPERIENCES PERÚ - SISTEMA DE GESTIÓN Y RESERVAS (MEP)   ")
    print("==================================================================")
    print("Iniciando servicios y demostración del catálogo de tarifas...\n")
    ejecutar_demo()
    print("\n[OK] Sistema inicializado y verificado correctamente en Docker/Local.")


if __name__ == "__main__":
    main()
