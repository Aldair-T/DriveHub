import os


def tipos_archivos() -> None:
    print("1) Crear una carpeta\n"
          "2) Crear un archivo .txt\n"
          "3) Crear un archivo .csv\n")


def crear_carpeta() -> None:
    nombre_carpeta = input("Ingrese el nombre de la carpeta: ")
    if os.path.isdir(nombre_carpeta):
        print("la carpeta existe")
    else:
        os.mkdir(nombre_carpeta)


def crear_archivo_txt() -> None:
    nombre_archivo = input("Ingrese el nombre del nuevo archivo: ")
    nombre_archivo += ".txt"
    nuevo_archivo = open(nombre_archivo, "w")
    nuevo_archivo.close()


def crear_archivo_csv() -> None:
    nombre_archivo = input("Ingres el nombre del nuevo archivo: ")
    nombre_archivo += ".csv"
    nuevo_archivo = open(nombre_archivo, "w")
    nuevo_archivo.close()


def creacion_archivos() -> None:
    tipos_archivos()
    opcion = input("Que quieres crear: ")
    while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > 3:
        opcion = input("Ingrese una opcion correcta: ")
    if int(opcion) == 1:
        crear_carpeta()
    elif int(opcion) == 2:
        crear_archivo_txt()
    else:
        crear_archivo_csv()