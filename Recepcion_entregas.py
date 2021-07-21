from pathlib import Path
from service_gmail import obtener_servicio
import os

def enviar_mensaje():
    gmail_de = "ljun@fi.uba.ar"
    gmail_para = "ljun@fi.uba.ar"
    asunto ="La entrega fue..."
    mensaje ="La entrega fue exitosa"

    message = MIMEText(mensaje)
    message['to'] = gmail_para
    message['from'] = gmail_de
    message['subject'] = asunto
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def main():
    enviar_mensaje()
    
