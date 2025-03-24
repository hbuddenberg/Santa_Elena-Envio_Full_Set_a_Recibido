import logging
from modules.configuracion import Configuracion as Configuracion_Yaml
from modules.extraer_excel import Configuracion as Configuracion_Excel
from modules.buscar_carpeta import buscar_carpeta
from modules.mover_carpeta import eliminar_carpetas, mover, mover_todo
from modules.listar_archivos import listar_archivos
from modules.estructurar_registro import estructurar
from modules.email_sender import enviar_reciver, enviar_informe, enviar_vacio
from modules.informe import genera_informe
from modules.compresor import validar_archivos
from datetime import datetime
from time import sleep
from pprint import pp
import os

# Configuración del registro de log
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = os.path.join(log_dir, f"execution_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
logging.basicConfig(filename=log_filename, level=print, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_GLOBAL = Configuracion_Yaml('src/configuration/configuracion.yaml')
CONFIG_EXCEL  = Configuracion_Excel(CONFIG_GLOBAL.config.path.shared.config)

def mover_carpetas_enproceso(ruta):
    print(f"Iniciando el proceso de mover carpetas en la ruta: {ruta}")
    archivos = None
    carpetas = None
    lista_carpetas = buscar_carpeta(ruta)
    if 'Configuracion' in lista_carpetas:
        lista_carpetas.remove('Configuracion')
    if 'En Proceso' in lista_carpetas:
        lista_carpetas.remove('En Proceso')
    if 'Listo' in lista_carpetas:
        lista_carpetas.remove('Listo')
    print(f"Carpetas encontradas: {lista_carpetas}")
    if len(lista_carpetas) > 0:
        print("Se encontraron carpetas en la ruta.")
        eliminar_carpetas(ruta)
        mover_carpetas = mover(ruta, lista_carpetas)
        if mover_carpetas:
            print("Carpetas movidas correctamente.")
            carpetas = listar_archivos(f'{ruta}/En Proceso')
        else:
            logging.error("Error al mover las carpetas.")
    if carpetas == None or len(carpetas) == 0:
        registros = None
    else:
        registros = {'ruta': {'raiz': ruta, 'en_proceso': f'{ruta}/En Proceso'}, 'carpetas': carpetas}
    return registros

def listar_carpetas(registros: dict):
    print("Listando carpetas en proceso.")
    ruta = registros['ruta']['en_proceso']
    if registros != None:
        if registros['carpetas'] != None:
            carpetas = registros['carpetas']
            print(f"Carpetas encontradas: {carpetas}")
        else:
            logging.warning(f"No se encontró un archivo PDF Instructivo en la carpeta {ruta}")
    else:
        logging.warning("No se encontró un archivo PDF Instructivo en la carpeta.")

    if carpetas == []:
        carpetas = None

    return ruta, carpetas

def generacion_informe(registros, ruta):
    print("Generando informe.")
    nombre_archivo = f"Informe_Envio_Recibidor_{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.xlsx"
    for registro in registros:
        archivo_informe = genera_informe(registro, ruta, nombre_archivo)
    return archivo_informe

def registros(carpetas: dict):
    lista_ejecucion = []
    print("Iniciando el proceso de registros.")
    for folder, files in carpetas['carpetas'].items():
        print(f"Ejecutando: {folder}")
        print(f"Archivos: {files}")
        ruta = f"{carpetas['ruta']['en_proceso']}/{folder}"
        files, tamaño_total = validar_archivos(files, ruta, folder)
        print(f"Tamaño total de los archivos: {tamaño_total} MB")
        estructura = estructurar(folder, files, CONFIG_EXCEL)
        print(f"Estructura: {estructura.to_dict()}")
        if estructura.emails_para not in (None, ''):
            if tamaño_total <= 25:
                status = enviar_reciver(CONFIG_GLOBAL, ruta, files, estructura, 'api')
            else:
                status = enviar_reciver(CONFIG_GLOBAL, ruta, files, estructura, 'api')
                status = {'estado': False, 'descripcion': f'Archivos mayores a 25MB, tamaño total {tamaño_total} MB'}
            print(f"Estado Correo: {status}")
        else:
            print(f"Correo para: {estructura.emails_para}")
            status = {'estado': False, 'descripcion': f'Correos de Recibidor o Recibidor no encontrado.'}

        lista_ejecucion.append({
            'carpeta': folder,
            'ruta': ruta,
            'archivos': files,
            'estructura': estructura.to_dict(),
            'estado_correo': status
        })

    if len(lista_ejecucion) > 0:
        sleep(1)
        archivo_informe = generacion_informe(lista_ejecucion, carpetas['ruta']['en_proceso'])
        enviar_informe(CONFIG_GLOBAL, CONFIG_EXCEL, archivo_informe, lista_ejecucion, 'api')
        mover_todo(CONFIG_GLOBAL.config.path.shared.main)

    return lista_ejecucion

def ejecutar():
    print("Ejecutando el proceso principal.")
    carpetas = mover_carpetas_enproceso(CONFIG_GLOBAL.config.path.shared.main)
    if carpetas != None:
        if len(carpetas['carpetas']) > 0:
            registros(carpetas)
        else:
            enviar_vacio(CONFIG_GLOBAL, CONFIG_EXCEL, 'api')
    else:
        enviar_vacio(CONFIG_GLOBAL, CONFIG_EXCEL, 'api')

def main():
    print("Iniciando el programa.")
    ejecutar()

if __name__ == "__main__":
    main()