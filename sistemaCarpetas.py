from service_drive import obtener_servicio as SERVICE_DRIVE
from service_gmail import obtener_servicio as SERVICE_GMAIL

carpeta_TP2_ID = "1356xXW9laVirDDJv1dEKgkAnw5zT1Rc3"

def carpetas_encontradas():
    carpetas_examenes_encontradas = list()
    arpetas_alumnos_encontradas = list()
    arpetas_profesores_encontradas = list()

    carpetas = SERVICE_DRIVE().files().list(q = f"mimeType = 'application/vnd.google-apps.folder' and parents in '{carpeta_TP2_ID}'").execute()

    print(carpetas)

    for carpeta in carpetas['files']:
        print(carpeta['name'])
    
    

def creacion_carpeta(nombre):

    file_metadata = {
        'name': nombre,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents' : [f'{carpeta_TP2_ID}']
    }

    carpeta_examenes = SERVICE_DRIVE().files().create(body=file_metadata).execute()

    carpeta_examenes_ID = carpeta_examenes.get('id')

    carpeta_profesores_metadata = {
        'name': "profesores",
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [carpeta_examenes_ID]
    }

    carpeta_profesores = SERVICE_DRIVE().files().create(body=carpeta_profesores_metadata).execute()

    carpeta_profesores_ID = carpeta_profesores.get('id')

    carpeta_alumnos_metadata = {        
        'name': "alumnos",
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [carpeta_profesores_ID]      
    }
    
    SERVICE_DRIVE().files().create(body=carpeta_alumnos_metadata).execute()



def leer_mail():

    resultados = SERVICE_GMAIL().users().messages().list(userId='me').execute()

    id_mails = []
    contador = 0

    for mail in resultados:
        mail_ID = (resultados['messages'][contador]['id'])
        id_mails.append(mail_ID)
        contador += 1

    for id_mail in id_mails:

        mail = SERVICE_GMAIL().users().messages().get(userId='me', id=id_mail, format='full').execute()

        for value in mail['payload']['headers']:
            if value['name'] == 'Subject':
                asunto = (value['value']).split()
                if asunto[0] == "nombre_examen":
                    nombre_examen = asunto[1]
                    creacion_carpeta(nombre_examen)



carpetas_encontradas()

leer_mail()



