import os
from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload
from ListadoArchivos import repo_local
from DescargarArchivos import tipos_archivos, elegir_extension


def subir_a_unidad(nombre: str, ruta_archivo: str, tipo_archivo: str) -> None:
    file_metadata = {'name': nombre, 'mimeType': tipo_archivo}
    media = MediaFileUpload(ruta_archivo, mimetype = tipo_archivo)
    obtener_servicio().files().create(body = file_metadata,
                                      media_body = media,
                                      fields = 'id').execute()
    print("Su archivo se subió con éxito")


def subir_a_carpeta_especifica(nombre: str, id_carpeta: str, ruta_archivo: str, tipo_archivo: str) -> None:
    file_metadata = {'name': nombre, 'mimeType': tipo_archivo, 'parents': [id_carpeta]}
    media = MediaFileUpload(ruta_archivo, mimetype = tipo_archivo)
    obtener_servicio().files().create(body = file_metadata,
                                      media_body = media,
                                      fields = 'id').execute()
    print("Su archivo se subió con exito")


def verificar_carpetas_drive(nombre: str, id_carpet: str, ruta_archivo: str, tipo_archivo: str) -> None:
    id_carpetas = []
    response = obtener_servicio().files().list(q = "mimeType = 'application/vnd.google-apps.folder'").execute()
    for file in response.get('files', []):
        ids = file.get('id')
        id_carpetas.append(ids)
    if id_carpet in id_carpetas:
        subir_a_carpeta_especifica(nombre, id_carpet, ruta_archivo, tipo_archivo)
    else:
        print("Esa carpeta no existe")


def elegir_datos(ruta_archivo: str, tipo_archivo: str) -> None:
    nombre = input("Ingrese el nombre para el nuevo archivo: ")
    respuesta = input("Deseas guardar en una carpeta especifica? s/n: ")
    if respuesta == "s":
        carpeta = input("Ingrese el id de su carpeta: ")
        verificar_carpetas_drive(nombre, carpeta, ruta_archivo, tipo_archivo)
    elif respuesta == "n":
        subir_a_unidad(nombre, ruta_archivo, tipo_archivo)
    else:
        print("Ingrese una opcion correcta")


def subir_archivos() -> None:
    print("Ingrese la ruta de su archivo")
    ruta_archivo = repo_local()
    tipos_archivos()
    tipo_archivo = input("Ingrese el tipo de archivo: ")
    while not tipo_archivo.isnumeric() or int(tipo_archivo) < 1 or int(tipo_archivo) > 8:
        tipo_archivo = input("Ingrese una opcion correcta: ")
    tipo_archivo = elegir_extension(tipo_archivo)
    if os.path.isfile(ruta_archivo):
        elegir_datos(ruta_archivo, tipo_archivo[0])
    else:
        print("Ese archivo no existe")
