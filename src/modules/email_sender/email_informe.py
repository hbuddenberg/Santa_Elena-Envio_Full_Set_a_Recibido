from .email_sender import enviar_correo_api, envio_correo_smtp
from datetime import datetime
import os

def enviar_informe(configuracion, excel, archivo_informe, lista_ejecucion, tipo='api'):
    if tipo not in ['smtp', 'api']:
        raise ValueError("El tipo de envío debe ser 'smtp' o 'api'.")

    asuntos_exitosos = [ejecucion['carpeta'] for ejecucion in lista_ejecucion if ejecucion['estado_correo']['estado']]

    asuntos_exitosos = [f"<li>{ejecucion}</li>" for ejecucion in asuntos_exitosos]

    asunto = f'Informe de ejecucion Envio Correo a Recibidores - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

    with open(configuracion.config.mail.template.report, 'r') as file:
        cuerpo_html = file.read()

    cuerpo_html = str(cuerpo_html).replace('{asuntos_exitosos}', ''.join(asuntos_exitosos))

    destinatarios = [email.strip() for email in excel.config.email_reporte[0].lista_emails.replace(';', ',').split(',')]
    copia = [email.strip() for email in configuracion.config.mail.sender.report.cc.replace(';', ',').split(',')]
    oculto = [email.strip() for email in configuracion.config.mail.sender.report.cco.replace(';', ',').split(',')]

    if tipo == 'api':
        status = enviar_correo_api(configuracion, destinatarios, asunto, cuerpo_html, [archivo_informe], copia, oculto)
    else:
        status = envio_correo_smtp(configuracion, configuracion.config.mail.config.smtp, destinatarios, asunto, cuerpo_html, [archivo_informe], copia, oculto)
    
    return status
'''
import sys
import os

#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append('/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido')

from src.modules.configuracion import Configuracion as Configuracion_Yaml
from src.modules.extraer_excel import Configuracion as Configuracion_Excel
from src.modules.estructurar_registro import estructurar

CONFIG_GLOBAL = Configuracion_Yaml('src/configuration/configuracion.yaml')
CONFIG_EXCEL = Configuracion_Excel(CONFIG_GLOBAL.config.path.shared.config)

folder = 'FULL SET OF DOCS OE232400007- MSC CASSANDRE- DIVINE (ETA 03-02-2024)'
ruta = '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS OE232400007- MSC CASSANDRE- DIVINE (ETA 03-02-2024)'
files = ['FULL SET OE232400007- MSC CASSANDRE- DIVINE.pdf', 'PACKING LIST OE232400007_MSC CASSANDRE_DIVINE FLAVOR LLC.xls']

estructura = estructurar(folder, files, CONFIG_EXCEL)

enviar_reciver(CONFIG_GLOBAL, ruta, files, estructura, 'api')
'''