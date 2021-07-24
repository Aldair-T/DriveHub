import os
import io
from googleapiclient.http import MediaIoBaseDownload
from service_drive import obtener_servicio


def tipos_archivos() -> None:
    print("1)Pdf\n"
          "2)Comprimido\n"
          "3)Text\n"
          "4)Csv\n"
          "5)Word\n"
          "6)Imagen\n"
          "7)PowerPoint\n"
          "8)Excel\n")


def elegir_extencion(archivo_elegido: str) -> list:
    if int(archivo_elegido) == 1:
        return ['application/pdf', '.pdf']
    elif int(archivo_elegido) == 2:
        return ['application/zip', '.zip']
    elif int(archivo_elegido) == 3:
        return ['text/plain', '.txt']
    elif int(archivo_elegido) == 4:
        return ['text/csv', '.csv']
    elif int(archivo_elegido) == 5:
        return ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx']
    elif int(archivo_elegido) == 6:
        return ['image/jpeg', '.jpg']
    elif int(archivo_elegido) == 7:
        return ['application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx']
    elif int(archivo_elegido) == 8:
        return ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx']


def descargar_archivos(ids_archivo: str, tipo_archivo: str, nombre_archivo: str) -> None:
    sheet_id = ids_archivo
    byteData = obtener_servicio().files().export_media(
        fileId = sheet_id,
        mimeType = tipo_archivo
    ).execute()
    with open(nombre_archivo, 'wb') as f:
        f.write(byteData)
        f.close()


def crear_nombre_archivo() -> None:
    ids_archivo = input("Ingrese el id de su archivo: ")
    nombre_archivo = input("Ingrese el nuevo nombre: ")
    tipos_archivos()
    tipo_a = input("Ingres el tipo de archivo: ")
    while not tipo_a.isnumeric() or int(tipo_a) < 1 or int(tipo_a) > 10:
        tipo_a = input("Ingrese una opcion correcta: ")
    tipo_a = elegir_extencion(tipo_a)
    nombre_archivo += tipo_a[1]
    descargar_archivos(ids_archivo, tipo_a[0], nombre_archivo)


def crear_carpeta_descargas() -> None:
    carpeta = 'Descargas_Drive'
    if os.path.isdir(carpeta):
        crear_nombre_archivo()
    else:
        os.mkdir(carpeta)
        crear_nombre_archivo()
