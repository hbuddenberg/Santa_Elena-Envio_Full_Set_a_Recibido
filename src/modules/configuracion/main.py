import os
import logging
import yaml
import json

class Configuracion():
    def __init__(self, archivo):
        self.set_by_yaml_file(archivo)

    def set_by_yaml_file(self, archivo):
        with open(archivo, 'r') as archivo:
            configuracion = yaml.safe_load(archivo)
        
        self.mapeo = configuracion['mapeo']
        self.ruta = configuracion['ruta']
        self.api = configuracion['api']
        self.correo = configuracion['correo']

    def get(self):
        logging.info("Obteniendo configuración")
        return self

    def get_dict(self):
        return {
                'mapeo': self.mapeo,
                'ruta': self.ruta,
                'api': {
                    'url': self.api['url'],
                    'key': self.api['key']
                },
                'correo': self.correo
            }

    def get_str(self):
        import json
        logging.info("Obteniendo configuración como string")
        return json.dumps(self, indent=4)

    def __str__(self):
        return self.get_str()

def main(archivo):
    configuracion = Configuracion(archivo)
    print(configuracion.get_dict())

if __name__ == "__main__":
    CONFIGURACION_PATH = 'src/configuration/configuracion.yaml'
    main(CONFIGURACION_PATH)