def menu() -> None:
    print("1) Listar archivos de la carpeta actual\n"
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
            pass
        if opcion == 2:
            pass
        if opcion == 3:
            pass
        if opcion == 4:
            pass
        if opcion == 5:
            pass
        if opcion == 6:
            pass
        if opcion == 7:
            pass
        if opcion == 8:
            acceso = False


main()