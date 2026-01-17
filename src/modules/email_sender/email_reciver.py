from .email_sender import enviar_correo_api, envio_correo_smtp
from datetime import datetime
import os

def enviar_reciver(configuracion, ruta, files, estructura, tipo='api'):
    if tipo not in ['smtp', 'api']:
        raise ValueError("El tipo de envío debe ser 'smtp' o 'api'.")

    with open(configuracion.config.mail.template.receiver, 'r') as file:
        cuerpo_html = file.read()

    cuerpo_html = str(cuerpo_html).replace('{cuerpo}', ''.join(estructura.cuerpo))

    archivos = [os.path.join(ruta, file) for file in files]

    destinatarios = [email.strip() for email in estructura.emails_para.replace(';', ',').split(',')]
    copia = [email.strip() for email in estructura.emails_copia.replace(';', ',').split(',')]
    oculto = [email.strip() for email in configuracion.config.mail.sender.report.cco.replace(';', ',').split(',')]

    if tipo == 'api':
        status = enviar_correo_api(configuracion, destinatarios, estructura.asunto, cuerpo_html, archivos, copia, oculto)
    else:
        status = envio_correo_smtp(configuracion, configuracion.config.mail.config.smtp, destinatarios, estructura.asunto, cuerpo_html, archivos, copia, oculto)

    return status
'''
import sys
import os

#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append('D:/Dev/Santa_Elena-Envio_Full_Set_a_Recibido')

from src.modules.configuracion import Configuracion as Configuracion_Yaml
from src.modules.extraer_excel import Configuracion as Configuracion_Excel
from src.modules.estructurar_registro import estructurar

CONFIG_GLOBAL = Configuracion_Yaml('src/configuration/configuracion.yaml')
CONFIG_EXCEL = Configuracion_Excel(CONFIG_GLOBAL.config.path.shared.config)

folder = 'FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)'
ruta = 'D:/Dev/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)'
files = ['FULL SET OE232400596- MAERSK BULAN - TROPME-1.pdf', 'FULL SET OE232400596- MAERSK BULAN - TROPME.pdf', 'FULL SET OE232400597- MAERSK BULAN - TROPME.pdf', 'PACKING LIST  - OE232400597_MAERSK BULAN_TROPME.xls', 'PACKING LIST - OE232400598_MAERSK BULAN_TROPME.xls', 'PACKING LIST - OE232400599_MAERSK BULAN_TROPME.xls']

estructura = estructurar(folder, files, CONFIG_EXCEL)

enviar_reciver(CONFIG_GLOBAL, ruta, files, estructura, 'api')
'''