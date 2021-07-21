from googleapiclient.http import MediaFileUpload


acceso = True

    input("Ingrese el nombre del archivo: ")
    if
    file_metadata = {'name': 'aldair.txt'}
    media = MediaFileUpload('aldair.txt', mimetype = 'text/txt')
    file = obtener_servicio().files().create(body = file_metadata,
                                             media_body = media,
                                             fields = 'id').execute()
    print('File ID: %s' % file.get('id'))