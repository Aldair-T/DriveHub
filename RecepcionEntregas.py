from service_gmail import obtener_servicio 
import base64
from email.mime.text import MIMEText
from email import errors

def enviar_mensaje():
    gmail_de = "ljun@fi.uba.ar"
    gmail_para = "ljun@fi.uba.ar"
    asunto ="La entrega fue..."
    mensaje ="La entrega fue exitosa"

    message = MIMEText(mensaje)
    message['to'] = gmail_para
    message['from'] = gmail_de
    message['subject'] = asunto
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body= {'raw': raw}

    try:
        message = (obtener_servicio.users().messages().send(userId='me', body=body).execute())
        print ("Mensaje enviado")
    except errors.MessageError as error:
        print ('An error occurred: %s' % error)
