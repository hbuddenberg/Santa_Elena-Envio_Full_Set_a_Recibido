import sys
import os

# Agrega el directorio raíz del proyecto ('src') al PYTHONPATH
# para permitir importaciones como 'from models import ...' que se usan en el código actual
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)
