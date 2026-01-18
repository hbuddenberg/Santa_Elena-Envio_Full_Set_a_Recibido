import pytest
import os
from modules.google_api.client import DriveClient
from modules.google_api.service import DriveService
from modules.configuracion import Configuracion

# Cargar configuración para obtener rutas de credenciales
CONFIG_PATH = "src/configuration/configuracion.yaml"

@pytest.fixture(scope="module")
def drive_service():
    """Fixture para crear y autenticar el servicio de Drive."""
    if not os.path.exists(CONFIG_PATH):
        pytest.skip(f"Archivo de configuración no encontrado: {CONFIG_PATH}")
    
    config_obj = Configuracion(CONFIG_PATH)
    config = config_obj.get_config()
    
    creds_path = config.mail.config.api.credentials
    token_path = config.mail.config.api.token
    scopes = config.mail.config.api.scopes + ['https://www.googleapis.com/auth/drive']

    if not os.path.exists(creds_path):
         pytest.skip(f"Credenciales no encontradas en {creds_path}. Se requiere autenticación real para este test.")
    
    if not os.path.exists(token_path):
        pytest.skip(f"Token no encontrado en {token_path}. Ejecuta el script manualmente una vez para autenticar.")

    client = DriveClient(creds_path, token_path, scopes)
    return DriveService(client)

def test_drive_authentication(drive_service):
    """Prueba que el servicio se crea correctamente."""
    assert drive_service.service is not None

def test_list_files(drive_service):
    """Prueba listar archivos en la carpeta raíz configurada."""
    config_obj = Configuracion(CONFIG_PATH)
    root_path_name = config_obj.get_config().path.drive.root_path
    
    try:
        root_id = drive_service.find_folder_id_by_path(root_path_name)
        assert root_id is not None
        
        # Listar contenido
        files = drive_service.list_folders_in_folder(root_id)
        assert isinstance(files, list)
        print(f"Encontrados {len(files)} ítems en {root_path_name}")
        
    except FileNotFoundError:
        pytest.fail(f"No se encontró la carpeta raíz: {root_path_name}")
    except Exception as e:
        pytest.fail(f"Error al listar archivos: {e}")
