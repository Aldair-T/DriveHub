import os
from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload


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
        return ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'docx']
    elif int(archivo_elegido) == 6:
        return ['image/jpeg', '.jpg']
    elif int(archivo_elegido) == 7:
        return ['application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx']
    elif int(archivo_elegido) == 8:
        return ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx']


def subiendo_archivo(archivo: str) -> None:
    archivos_metadata = {'name': archivo}
    media = MediaFileUpload(archivo)
    obtener_servicio().files().create(body = archivos_metadata,
                                      media_body = media,
                                      fields = 'id').execute()
    print("Archivo subido con éxito")


def subir_archivos() -> None:
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    tipos_archivos()
    tipo_a = input("Ingrese el tipo de archivo: ")
    while not tipo_a.isnumeric() or int(tipo_a) < 1 or int(tipo_a) > 10:
        tipo_a = input("Ingrese una opcion correcta: ")
    tipo_a = elegir_extencion(tipo_a)
    nombre_archivo += tipo_a[1]
    if os.path.exists(nombre_archivo[1]):
        subiendo_archivo(nombre_archivo[1])
    else:
        print("Ese archivo no existe")
