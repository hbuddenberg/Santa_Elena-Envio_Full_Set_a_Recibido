import pprint

from models import load_config_yaml as load_config


class Configuracion:
    def __init__(self, archivo_configuracion):
        self.path_file = archivo_configuracion
        self.config = load_config(archivo_configuracion)

    def get_config(self):
        return self.config

    def get_dict(self):
        return self.config.model_dump()

    def get_path_file(self):
        return self.path_file


def main(configuracion_path):
    configuracion = Configuracion(configuracion_path)
    pprint.pp(configuracion.get_dict())


if __name__ == "__main__":
    CONFIGURACION_PATH = "src/configuration/configuracion.yaml"
    main(CONFIGURACION_PATH)
