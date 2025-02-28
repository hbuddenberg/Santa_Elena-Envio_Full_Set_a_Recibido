import os
import shutil
import logging
from datetime import datetime

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def validar_ruta(ruta):
    """
    Valida si la ruta existe.
    """
    if not os.path.exists(ruta):
        logging.error(f"La ruta {ruta} no existe.")
        raise FileNotFoundError(f"La ruta {ruta} no existe.")
    if not os.path.isdir(ruta):
        logging.error(f"La ruta {ruta} no es un directorio.")
        raise NotADirectoryError(f"La ruta {ruta} no es un directorio.")
    logging.info(f"Ruta {ruta} validada correctamente.")

def eliminar_carpetas(ruta):
    destino_base = os.path.join(ruta, 'En Proceso')
    if os.path.exists(destino_base):
        for item in os.listdir(destino_base):
            item_path = os.path.join(destino_base, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logging.info(f"Carpeta {item_path} eliminada.")
            else:
                os.remove(item_path)
                logging.info(f"Archivo {item_path} eliminado.")
    else:
        logging.info(f"La carpeta {destino_base} no existe.")

def mover_carpetas(ruta, lista_carpeta):
    """
    Mueve las carpetas especificadas en lista_carpeta a la ruta destino.
    """
    destino_base = os.path.join(ruta, 'En Proceso')
    if not os.path.exists(destino_base):
        os.makedirs(destino_base)
        logging.info(f"Carpeta de destino {destino_base} creada.")

    for carpeta in lista_carpeta:
        origen = os.path.join(ruta, carpeta)
        destino = os.path.join(destino_base, carpeta)
        if os.path.exists(origen):
            shutil.move(origen, destino)
            logging.info(f"Carpeta {carpeta} movida a {destino}.")
        else:
            logging.warning(f"La carpeta {carpeta} no existe en la ruta {ruta}.")
def mover(ruta, lista_carpeta):
    """
    Función principal que recibe los argumentos y ejecuta las acciones.
    """
    try:
        validar_ruta(ruta)
        mover_carpetas(ruta, lista_carpeta)
        mover = True
    except Exception as e:
        mover = False
        logging.error(f"Error en la ejecución: {e}")
    return mover

def mover_todo(ruta):
        destino_base = os.path.join(ruta, 'En Proceso')
        destino_final = os.path.join(ruta, 'Listo', datetime.now().strftime('%Y-%m-%d'),datetime.now().strftime('%H.%M.%S'))
        if not os.path.exists(destino_final):
            os.makedirs(destino_final)
            logging.info(f"Carpeta de destino final {destino_final} creada.")
        
        for item in os.listdir(destino_base):
            origen = os.path.join(destino_base, item)
            destino = os.path.join(destino_final, item)
            if os.path.exists(origen):
                shutil.move(origen, destino)
                logging.info(f"Elemento {item} movido a {destino}.")
            else:
                logging.warning(f"El elemento {item} no existe en la ruta {destino_base}.")
        
        print(f"Elementos movidos correctamente a la carpeta {destino_final}.")

def main(ruta, lista_carpeta):
    """
    Función principal que recibe los argumentos y ejecuta las acciones.
    """
    try:
        validar_ruta(ruta)
        mover_carpetas(ruta, lista_carpeta)
        mover = True
    except Exception as e:
        mover = False
        logging.error(f"Error en la ejecución: {e}")
    return mover

if __name__ == "__main__":
    ruta = '/Volumes/Resources/Development/SmartBots/Santa_Helena-Subida_Archivos_a_Agente_Aduana/test/resources'
    mover_todo(ruta)