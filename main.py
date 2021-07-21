from ListadoArchivos import listar_archivos
from CrearArchivos import creacion_archivos
from DescargarArchivos import descargar_archivos
from SubirArchivo import subir_archivos


def menu() -> None:
    print("1) Listar archivos\n"
          "2) Crear un archivo\n"
          "3) Subir un archivo\n"
          "4) Descargar un archivo\n"
          "5) Sincronizar\n"
          "6) Genera carpeta de una evaluacion\n"
          "7) Actualizar entregas de alumnos via mail\n"
          "8) Salir")


def opcion_valida(opcion: str) -> int:
    while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > 8:
        opcion = input("Ingrese una opcion correcta: ")
    opcion = int(opcion)
    return opcion


def main() -> None:
    menu()
    acceso = True
    opcion = input("Ingrese una opcion: ")
    opcion = opcion_valida(opcion)
    while acceso == True:
        if opcion == 1:
            listar_archivos()
        if opcion == 2:
            creacion_archivos()
        if opcion == 3:
            subir_archivos()
        if opcion == 4:
            descargar_archivos()
        if opcion == 5:
            pass
        if opcion == 6:
            pass
        if opcion == 7:
            pass
        if opcion == 8:
            acceso = False


main()
