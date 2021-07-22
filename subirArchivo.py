import os
from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload



def subiendo_archivo(archivo: str) -> None:
    archivo_metadata = {'name': archivo}
    media = MediaFileUpload(archivo)
    obtener_servicio().files().create(body = archivo_metadata,
                                      media_body = media,
                                      fields = 'id').execute()
    print("Archivo subido con éxito")


def subir_archivos() -> None:
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    tipo_archivo = input("Ingrese el tipo de archivo: ")
    archivo = nombre_archivo + tipo_archivo
    if os.path.exists(archivo):
        subiendo_archivo(archivo)
    else:
        print("Ese archivo no existe")