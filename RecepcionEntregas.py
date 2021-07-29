from service_drive import obtener_servicio as SERVICE_DRIVE


def buscar_carpeta(nombre_alumno: str, archivo) ->  None:
    id_ = input("Ingrese el nombre de la carpeta: ")
    carpetas_en_drive = {}
    carpetas_profesores = {}
    carpetas_alumnos = {}
    carpetas = SERVICE_DRIVE().files().list(q = "mimeType = 'application/vnd.google-apps.folder'",
                                            fields = 'files(id, name)').execute()
    for carpeta in carpetas['files']:
        nombre = carpeta.get('name')
        id_carpeta = carpeta.get('id')
        carpetas_en_drive[nombre] = id_carpeta
    for clave, valor in carpetas_en_drive.items():
        if id_ == clave:
            query = f"parents = '{valor}' and mimeType = 'application/vnd.google-apps.folder'"
            respuesta = SERVICE_DRIVE().files().list(q = query,
                                                     fields = 'files(id, name)').execute()
            for archivos in respuesta.get('files', []):
                nombre_carpeta = archivos.get('name')
                carpeta_evaluacion = archivos.get('id')
                carpetas_profesores[nombre_carpeta] = carpeta_evaluacion
    for clave, valor in carpetas_profesores.items():
        query2 = f"parents = '{valor}' and mimeType = 'application/vnd.google-apps.folder'"
        respuesta2 = SERVICE_DRIVE().files().list(q = query2,
                                                  fields = 'files(id, name)').execute()
        for carpeta_alum in respuesta2.get('files', []):
            nombre_carpeta_alum = carpeta_alum.get('name')
            carpeta_id_alum = carpeta_alum.get('id')
            carpetas_alumnos[nombre_carpeta_alum] = carpeta_id_alum
    for clave, valor in carpetas_alumnos.items():
        if clave == nombre_alumno:
            print("El archivo tiene q pasar de gmail a drive")

buscar_carpeta()