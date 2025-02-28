from datetime import datetime
import pandas as pd
import os

def genera_informe(registro, ruta, nombre_archivo):
    # Crear un DataFrame vacío
    df = pd.DataFrame()

    # Agregar los datos del registro al DataFrame
    df = pd.DataFrame([{
        'Asunto': registro['estructura']['asunto'],
        'Recibidor': registro['estructura']['recibidor'],
        'cuerpo': registro['estructura']['cuerpo'].replace('<br>','').replace('<b>','').replace('</b>',''),
        'Adjuntos': ', '.join(registro['estructura']['adjuntos']),
        'Emails Para': registro['estructura']['emails_para'],
        'Estado Envio': 'OK' if registro['estado_correo']['estado'] else 'ERROR',
        'Descripcion Envio': registro['estado_correo']['descripcion'],
        'Fecha Envio': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])

    # Ruta del archivo
    ruta_archivo = f"{ruta}/{nombre_archivo}"

    # Verificar si el archivo ya existe
    if os.path.exists(ruta_archivo):
        # Cargar el archivo existente
        df_existente = pd.read_excel(ruta_archivo)
        # Concatenar los datos nuevos con los existentes
        df = pd.concat([df_existente, df], ignore_index=True)

    # Guardar el DataFrame en un archivo Excel en la ruta especificada
    df.to_excel(ruta_archivo, index=False)

    print(f"Archivo Excel generado y guardado en: {ruta_archivo}")

    return ruta_archivo

def main(registro, ruta):
    pass

if __name__ == "__main__":
    registros = [{'carpeta': 'FULL SET OF DOCS OE232400007- MSC CASSANDRE- DIVINE (ETA 03-02-2024)', 'ruta': '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS OE232400007- MSC CASSANDRE- DIVINE (ETA 03-02-2024)', 'archivos': ['FULL SET OE232400007- MSC CASSANDRE- DIVINE.pdf', 'PACKING LIST OE232400007_MSC CASSANDRE_DIVINE FLAVOR LLC.xls'], 'estructura': {'recibidor': 'DIVINE', 'pais': 'USA-Canada', 'emails_para': 'h.buddenberg@gmail.com', 'emails_copia': 'h.buddenberg@gmail.com', 'adjuntos': ['FULL SET OE232400007- MSC CASSANDRE- DIVINE.pdf', 'PACKING LIST OE232400007_MSC CASSANDRE_DIVINE FLAVOR LLC.xls'], 'asunto': 'FULL SET OF DOCS OE232400007- MSC CASSANDRE- DIVINE (ETA 03-02-2024)', 'cuerpo': 'Dear <br>\nPlease find attached The Following docs : <br>\n<br>\n- Bill of Lading (SWB) <br>\n- Invoice<br>\n - Certificate Of Origin <br>\n- Phytosanitary certificate <br>\n- Packing List <br>\n<br>\n<b>Docs are send only by Email, if you need docs phisically please advise, Thanks!<br>\n In case of questions, send email to comex@santaelena.com, comex2@santaelena.com, comexasistente@santaelena.com  <br>\n<br>\nBest Regards!! </b>'}, 'estado_correo': {'estado': True, 'descripcion': 'Correo enviado correctamente.'}}, {'carpeta': 'FULL SET OF DOCS OE232400514- MSC BIANCA- METRO  (ETA 20-05-2024- Container: BMOU964791-5- PO 15398631)', 'ruta': '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS OE232400514- MSC BIANCA- METRO  (ETA 20-05-2024- Container: BMOU964791-5- PO 15398631)', 'archivos': ['FULL SET OE232400514 - MSC BIANCA - METRO.pdf', 'PACKING LIST OE232400514_MSC BIANCA_METRO.xls'], 'estructura': {'recibidor': 'METRO', 'pais': 'USA-Canada', 'emails_para': 'h.buddenberg@gmail.com', 'emails_copia': 'h.buddenberg@gmail.com', 'adjuntos': ['FULL SET OE232400514 - MSC BIANCA - METRO.pdf', 'PACKING LIST OE232400514_MSC BIANCA_METRO.xls'], 'asunto': 'FULL SET OF DOCS OE232400514- MSC BIANCA- METRO  (ETA 20-05-2024- Container: BMOU964791-5- PO 15398631)', 'cuerpo': 'Dear <br>\nPlease find attached The Following docs : <br>\n<br>\n- Bill of Lading (SWB) <br>\n- Invoice<br>\n - Certificate Of Origin <br>\n- Phytosanitary certificate <br>\n- Packing List <br>\n<br>\n<b>Docs are send only by Email, if you need docs phisically please advise, Thanks!<br>\n In case of questions, send email to comex@santaelena.com, comex2@santaelena.com, comexasistente@santaelena.com  <br>\n<br>\nBest Regards!! </b>'}, 'estado_correo': {'estado': True, 'descripcion': 'Correo enviado correctamente.'}}, {'carpeta': 'FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)', 'ruta': '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)', 'archivos': ['FULL SET OE232400596- MAERSK BULAN - TROPME-1.pdf', 'FULL SET OE232400596- MAERSK BULAN - TROPME.pdf', 'FULL SET OE232400597- MAERSK BULAN - TROPME.pdf', 'PACKING LIST  - OE232400597_MAERSK BULAN_TROPME.xls', 'PACKING LIST - OE232400598_MAERSK BULAN_TROPME.xls', 'PACKING LIST - OE232400599_MAERSK BULAN_TROPME.xls'], 'estructura': {'recibidor': 'TROPME', 'pais': 'Rusia-ALGO DE EUROPA', 'emails_para': 'h.buddenberg@gmail.com', 'emails_copia': 'h.buddenberg@gmail.com', 'adjuntos': ['FULL SET OE232400596- MAERSK BULAN - TROPME-1.pdf', 'FULL SET OE232400596- MAERSK BULAN - TROPME.pdf', 'FULL SET OE232400597- MAERSK BULAN - TROPME.pdf', 'PACKING LIST  - OE232400597_MAERSK BULAN_TROPME.xls', 'PACKING LIST - OE232400598_MAERSK BULAN_TROPME.xls', 'PACKING LIST - OE232400599_MAERSK BULAN_TROPME.xls'], 'asunto': 'FULL SET OF DOCS OE232400596 -OE232400597 -OE232400598 -OE232400599- MAERSK BULAN - TROPME (ETA 01-05-2024)', 'cuerpo': 'Dear <br>\nPlease find attached The Following docs : <br>\n<br>\n- Bill of Lading (SWB) <br>\n- Invoice<br>\n - Certificate Of Origin <br>\n- Phytosanitary certificate <br>\n- Packing List <br>\n<br>\n<b>I will appreciate if you can confirm to us the reception and approval of the sent documents. Once it´s done, I will proceed to send the original documents// Please Send email to <br> comex@santaelena.com, comex2@santaelena.com, comexasistente@santaelena.com <br>\n\nBest Regards!!</b><br>'}, 'estado_correo': {'estado': True, 'descripcion': 'Correo enviado correctamente.'}}, {'carpeta': 'FULL SET OF DOCS OE232401011 - MSC YASHI B - ALBERT HEIJN (ETA 10-05-2024)', 'ruta': '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS OE232401011 - MSC YASHI B - ALBERT HEIJN (ETA 10-05-2024)', 'archivos': ['FULL SET OE232401011- MSC YASHI B - ALBERT HEIJN - SANTA ELENA.pdf', 'PACKING LIST - OE232401011_MSC YASHI B_ALBERT HEIJN.xls'], 'estructura': {'recibidor': 'ALBERT HEIJN', 'pais': 'ALGUNOS DE EUROPA', 'emails_para': 'h.buddenberg@gmail.com', 'emails_copia': 'h.buddenberg@gmail.com', 'adjuntos': ['FULL SET OE232401011- MSC YASHI B - ALBERT HEIJN - SANTA ELENA.pdf', 'PACKING LIST - OE232401011_MSC YASHI B_ALBERT HEIJN.xls'], 'asunto': 'FULL SET OF DOCS OE232401011 - MSC YASHI B - ALBERT HEIJN (ETA 10-05-2024)', 'cuerpo': 'Dear <br>\nPlease find attached The Following docs : <br>\n<br>\n- Bill of Lading (SWB) <br>\n- Invoice<br>\n - Certificate Of Origin <br>\n- Phytosanitary certificate <br>\n- Packing List <br>\n<br>\n<br> I will dispatch original documents tomorrow, Thanks!! <br>\n<br>\nBest Regards!!</b><br>'}, 'estado_correo': {'estado': True, 'descripcion': 'Correo enviado correctamente.'}}]
    ruta = '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso'
    nombre_archivo = f"Informe_Envio_Recibidor_{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.xlsx"

    for registro in registros:
        archivo_informe = genera_informe(registro, ruta, nombre_archivo)