import os
from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload
from ListadoArchivos import repo_local


def tipos_archivos() -> None:
    print("1)Pdf\n"
          "2)Comprimido\n"
          "3)Text\n"
          "4)Csv\n"
          "5)Word\n"
          "6)Imagen\n"
          "7)PowerPoint\n"
          "8)Excel\n")


def elegir_extencion(archivo_elegido: str) -> str:
    if int(archivo_elegido) == 1:
        return 'application/pdf'
    elif int(archivo_elegido) == 2:
        return 'application/zip'
    elif int(archivo_elegido) == 3:
        return 'text/plain'
    elif int(archivo_elegido) == 4:
        return 'text/csv'
    elif int(archivo_elegido) == 5:
        return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif int(archivo_elegido) == 6:
        return 'image/jpeg'
    elif int(archivo_elegido) == 7:
        return 'application/vnd.openxmlforma ts-officedocument.presentationml.presentation'
    elif int(archivo_elegido) == 8:
        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


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
    nombre = input("Ingrese el nombre del nuevo archivo: ")
    respuesta = input("Deseas guardar en una carpeta especifica? s/n: ")
    if respuesta == "s":
        carpeta = input("Ingrese el id de su carpeta: ")
        subir_a_carpeta_especifica(nombre, carpeta, ruta_archivo, tipo_archivo)
    elif respuesta == "n":
        subir_a_unidad(nombre, ruta_archivo, tipo_archivo)
    else:
        print("Ingrese una opcion correcta")


def subir_archivos() -> None:
    print("Ingrese la ruta de su archivo")
    ruta_archivo = repo_local()
    tipos_archivos()
    tipo_archivo = input("Ingrese el tipo de archivo: ")
    while not tipo_archivo.isnumeric() or int(tipo_archivo) < 1 or int(tipo_archivo) > 10:
        tipo_archivo = input("Ingrese una opcion correcta: ")
    tipo_archivo = elegir_extencion(tipo_archivo)
    if os.path.isfile(ruta_archivo):
        elegir_datos(ruta_archivo, tipo_archivo)
    else:
        print("Ese archivo no existe")
