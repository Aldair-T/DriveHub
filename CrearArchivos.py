from pathlib import Path
from service_drive import obtener_servicio
from DescargarArchivos import elegir_extension
import os


def tipos_archivos() -> None:
    # Tipos de archivos que se pueden crear (Pueden faltar algunos)
    print("1) Crear un archivo .pdf\n"
          "2) Crear un archivo .zip\n"
          "3) Crear un archivo .txt\n"
          "4) Crear un archivo .csv\n"
          "5) Crear un archivo .jpg\n"
          "6) Crear un archivo PowerPoint\n"
          "7) Crear un archivo Word\n"
          "8) Crear un archivo Excel\n"
          "9) Crear una carpeta")


def crear_carpeta_drive(nombre_carpeta: str):
    archivo_metadata = {
        'name': nombre_carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    obtener_servicio().files().create(body = archivo_metadata, fields = 'id').execute()
    print("Se creo su carpeta")


def crear_carpeta() -> None:
    # Crea carpetas, falta que naveguen en el escritorio
    nombre_carpeta = input("Ingrese el nombre de la carpeta: ")
    if os.path.isdir(nombre_carpeta):
        print("la carpeta existe")
    else:
        crear_carpeta_drive(nombre_carpeta)
        os.mkdir(nombre_carpeta)


def crear_archivo_drive(tipo_archivo: str, nombre_archivo) -> None:
    archivo_metadata = {
        'name': nombre_archivo,
        'mimeType': tipo_archivo
    }
    obtener_servicio().files().create(body = archivo_metadata, fields = 'id').execute()


def crear_archivo_local(tipo_archivo: str, extension: str) -> None:
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    nombre_archivo += extension
    archivo = Path(nombre_archivo)
    if archivo.is_file():
        print("Ese archivo ya existe")
    else:
        crear_archivo_drive(tipo_archivo, nombre_archivo)
        nuevo_archivo = open(nombre_archivo, "w", encoding = "utf-8")
        nuevo_archivo.close()
        print("Se creo con éxito")


def creacion_archivos() -> None:
    # Es el menu para ver que archivo va a crear
    tipos_archivos()
    opcion = input("Que quieres crear: ")
    while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > 9:
        opcion = input("Ingrese una opcion correcta: ")
    extension = elegir_extension(opcion)
    if int(opcion) == 9:
        crear_carpeta()
    else:
        crear_archivo_local(extension[0], extension[1])
