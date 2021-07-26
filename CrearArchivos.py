from pathlib import Path
from service_drive import obtener_servicio
import os


def tipos_archivos() -> None:
    # Tipos de archivos que se pueden crear (Pueden faltar algunos)
    print("1) Crear una carpeta\n"
          "2) Crear un archivo .txt\n"
          "3) Crear un archivo .csv\n"
          "4) Crear un archivo .jpg\n"
          "5) Crear un archivo .pdf\n"
          "6) Crear un archivo Word\n"
          "7) Crear un archivo Excel\n"
          "8) Crear un archivo PowerPoint\n")


def crear_carpeta_drive(nombre_carpeta: str):
    archivo_metadata = {
        'name': nombre_carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    obtener_servicio().files().create(body= archivo_metadata, fields = 'id').execute()
    print("Se creo su carpeta")


def crear_carpeta() -> None:
    # Crea carpetas, falta que naveguen en el escritorio
    nombre_carpeta = input("Ingrese el nombre de la carpeta: ")
    if os.path.isdir(nombre_carpeta):
        print("la carpeta existe")
    else:
        crear_carpeta_drive(nombre_carpeta)
        os.mkdir(nombre_carpeta)


def crear_archivo_txt_drive(nombre_archivo):
    archivo_metadata = {
        'name': nombre_archivo,
        'mimeType': 'text/plain'
    }
    obtener_servicio().files().create(body = archivo_metadata, fields = 'id').execute()
    print("Se creo su archivo .txt")


def crear_archivo_txt() -> None:
    # Crea archivos .txt falta la navegacion
    nombre_archivo = input("Ingrese el nombre del nuevo archivo: ")
    nombre_archivo += ".txt"
    archivo = Path(nombre_archivo)
    if archivo.is_file():
        print("Ese nombre de archivo ya existe")
    else:
        crear_archivo_txt_drive(nombre_archivo)
        nuevo_archivo = open(nombre_archivo, "w", encoding = "utf-8")
        nuevo_archivo.close()


def crear_archivo_csv_drive(nombre_archivo):
    archivo_metadata = {
        'name': nombre_archivo,
        'mimeType': 'text/plain'
    }
    obtener_servicio().files().create(body = archivo_metadata, fields = 'id').execute()
    print("Se creo su archivo .csv")


def crear_archivo_csv() -> None:
    # Crea archivos .csv, falta la navegacion
    nombre_archivo = input("Ingres el nombre del nuevo archivo: ")
    nombre_archivo += ".csv"
    archivo = Path(nombre_archivo)
    if archivo.is_file():
        print("Ese nombre de archivo ya existe")
    else:
        crear_archivo_csv_drive(nombre_archivo)
        nuevo_archivo = open(nombre_archivo, "w", encoding = "utf-8")
        nuevo_archivo.close()


def creacion_archivos() -> None:
    # Es el menu para ver que archivo va a crear
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
