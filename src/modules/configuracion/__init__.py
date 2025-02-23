# Archivo de inicialización del módulo buscar_carpeta
try:
	from .main import Configuracion
except ImportError:
	raise ImportError("No se ha podido resolver la importación '.buscar'. Asegúrese de que el archivo 'buscar.py' existe en el directorio 'buscar_carpeta'.")

__all__ = ['main']