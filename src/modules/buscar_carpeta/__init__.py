# Archivo de inicialización del módulo buscar_carpeta
try:
	from .main import buscar
except ImportError:
	raise ImportError("No se ha podido resolver la importación '.buscar'. Asegúrese de que el archivo 'buscar.py' existe en el directorio 'buscar_carpeta'.")