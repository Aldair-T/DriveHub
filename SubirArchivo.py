from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload

'''id_carpeta = ""
nombre_archivos = [""]
tipo_archivos = [".jpg (etc)"]

for nombre_archivo, tipo_archivo in zip(nombre_archivos, tipo_archivos):
    file_metadata = {'name': "nombre", 'carpeta': [id_carpeta]}
    media = MediaFileUpload('files/photo.jpg', mimetype = 'image/jpeg')
    file = obtener_servicio().files().create(body = file_metadata,
                                             media_body = media,
                                             fields = 'id').execute()
    print('File ID: %s' % file.get('id'))
'''