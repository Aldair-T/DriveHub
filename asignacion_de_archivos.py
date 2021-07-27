from service_drive import obtener_servicio as SERVICE_DRIVE
from service_gmail import obtener_servicio as SERVICE_GMAIL
import csv

def leer_mail(carpetas_en_drive: list) -> None:

    resultados = SERVICE_GMAIL().users().messages().list(userId='me').execute()


    id_mails = []
    contador = 0
    
    for mail in resultados['messages']:
        mail_ID = (resultados['messages'][contador]['id'])
        id_mails.append(mail_ID)
        contador += 1

    for id_mail in id_mails:

        archivo = SERVICE_GMAIL().users().attachments().get(userId='me', messageId=id_mail, x__xgafv=None).execute()

        for padron in mail['payload']['headers']:
            #encajar padron con nombre y apellido


leer_mail()
