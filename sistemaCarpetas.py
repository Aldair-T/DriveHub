from service_drive import obtener_servicio



nombre = input("Ingrese nombre de carpeta")

def creacion_carpeta():
    file_metadata = {
        'name': nombre,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    obtener_servicio().files().create(body=file_metadata).execute()
                                    
                                            

creacion_carpeta()

