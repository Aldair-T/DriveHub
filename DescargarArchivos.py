import os
import io
from googleapiclient.http import MediaIoBaseDownload
from service_drive import obtener_servicio

# Es una maqueta, hay errores q no puedo resolverlo, no entiendo el metodo

'''servicio = obtener_servicio()
file_id = ['0BwwA4oUTeiV1UVNwOHItT0xfa2M']
file_name = ['hola']
for file_id, file_name in zip(file_id,file_name):
    request = servicio.files().get_media(fileId = file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download progress {0}" .format(status.progress() * 100))
'''