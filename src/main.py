from modules.configuracion import Configuracion
from modules.buscar_carpeta import buscar as buscar_carpeta
from modules.mover_carpeta import mover, mover_todo
from modules.listar_archivos import listar_archivos
from modules.email_sender import enviar_correo
from modules.informe import genera_informe
from datetime import datetime

CONFIGURACION_PATH = 'src/configuration/configuracion.yaml'

def ejecucion(configuracion: Configuracion):
    

def main():
    configuracion = Configuracion(CONFIGURACION_PATH)
    ejecucion(configuracion)

if __name__ == "__main__":
    main()