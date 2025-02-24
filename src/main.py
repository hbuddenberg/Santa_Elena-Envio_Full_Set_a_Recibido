from modules.configuracion import Configuracion as Configuracion_Yaml
from modules.extraer_excel import Configuracion as Configuracion_Excel
from modules.buscar_carpeta import buscar_carpeta
from modules.mover_carpeta import mover, mover_todo
from modules.listar_archivos import listar_archivos

from pprint import pp 

CONFIG_GLOBAL = Configuracion_Yaml('src/configuration/configuracion.yaml')
CONFIG_EXCEL  = Configuracion_Excel(CONFIG_GLOBAL.config.path.shared.config)

def mover_carpetas_enproceso(ruta):
    archivos = None
    lista_carpetas = buscar_carpeta(ruta)
    if 'Configuracion' in lista_carpetas:
        lista_carpetas.remove('Configuracion')
    if 'En Proceso' in lista_carpetas:
        lista_carpetas.remove('En Proceso')
    if 'Listo' in lista_carpetas:
        lista_carpetas.remove('Listo')
    print(f"Carpetas : {lista_carpetas}")
    if len(lista_carpetas) > 0:
        print("Se encontraron carpetas en la ruta.")
        mover_carpetas = mover(ruta, lista_carpetas)
        if mover_carpetas:
            print("Carpetas movidas correctamente.")
            archivos = listar_archivos(f'{ruta}/En Proceso')
        else:
            print("Error al mover las carpetas.")
    if archivos == None:
        registros = None
    else:
        registros = {'ruta': {'raiz': ruta, 'en_proceso': f'{ruta}/En Proceso'}, 'carpetas': archivos}
    return registros

def listar_carpetas(registros: dict):
    ruta = registros['ruta']['en_proceso']
    if registros != None:
        if registros['carpetas'] != None:
            carpetas = registros['carpetas']
            print(f"Carpetas : {carpetas}")
        else:
            print(f"No se encontró un archivo PDF Instructivo en la carpeta {ruta}")
    else:
        print(f"No se encontró un archivo PDF Instructivo en la carpeta.")

    if carpetas == []:
        carpetas = None

    return ruta, carpetas

def ejecutar():
    carpetas = mover_carpetas_enproceso(CONFIG_GLOBAL.config.path.shared.main)
    if carpetas != None:
        ruta, carpetas = listar_carpetas(carpetas)
        lista_ejecucion = []
        #for key, dict in carpetas.items():

def main():
    ejecutar()

if __name__ == "__main__":
    main()