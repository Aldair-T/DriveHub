from service_drive import obtener_servicio



nombre = input("Ingrese nombre de carpeta")

def creacion_carpeta():

    file_metadata = {
        'name': nombre,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    carpeta_examenes = obtener_servicio().files().create(body=file_metadata).execute()

    carpeta_examenes_ID = carpeta_examenes.get('id')

    carpeta_profesores_metadata = {
        'name': "profesores",
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [carpeta_examenes_ID]
    }

    carpeta_profesores = obtener_servicio().files().create(body=carpeta_profesores_metadata).execute()

    carpeta_profesores_ID = carpeta_profesores.get('id')

    carpeta_alumnos_metadata = {        
        'name': "alumnos",
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [carpeta_profesores_ID]      
    }
    
    obtener_servicio().files().create(body=carpeta_alumnos_metadata).execute()
                                    
                                            

creacion_carpeta()

